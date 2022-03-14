""" model_visitor.py """

from arpeggio import PTNodeVisitor

class SubsystemVisitor(PTNodeVisitor):

    # Elements
    def visit_nl(self, node, children):
        return None

    def visit_sp(self, node, children):
        return None

    def visit_mult(self, node, children):
        """Binary association (not association class) multiplicity"""
        mult = node.value  # No children because literal 1 or M is thrown out
        return mult

    def visit_acword(self, node, children):
        """All caps word"""
        return node.value  # No children since this is a literal

    def visit_icaps_name(self, node, children):
        """Model element name"""
        name = ''.join(children)
        return name

    def visit_class_name(self, node, children):
        """Class name"""
        name = ''.join(children)
        return {'name': name }

    def visit_keyletter(self, node, children):
        """Abbreviated keyletter name of class"""
        return { 'keyletter': children[0] }

    def visit_import(self, node, children):
        """Imported class marker"""
        d = {'import': children[0]}
        return d

    def visit_class_header(self, node, children):
        """Beginning of class section, includes name, optional keyletter and optional import marker"""
        items = {k: v for d in children for k, v in d.items()}
        return items

    def visit_subsystem_header(self, node, children):
        """Beginning of sybsystem section"""
        abbr = None if len(children) == 2 else children[1]
        return {'subsys_name': children[0], 'abbr': abbr, 'domain_name' : children[-1]}

    def visit_body_line(self, node, children):
        """Lines that we don't need to parse yet, but eventually will"""
        # TODO: These should be attributes and actions
        body_text_line = children[0]
        return body_text_line

    def visit_phrase(self, node, children):
        """Phrase on one side of a binary relationship phrase"""
        phrase = ''.join(children)
        return phrase

    def visit_assoc_class(self, node, children):
        """Association class name and multiplicity"""
        return { "assoc_mult": children[0], "assoc_cname": children[1] }

    def visit_t_side(self, node, children):
        """T side of a binary association"""
        return {node.rule_name: {"phrase": children[0], "mult": children[1], "cname": children[2]}}

    def visit_p_side(self, node, children):
        """P side of a binary association"""
        return {node.rule_name: {"phrase": children[0], "mult": children[1], "cname": children[2]}}

    def visit_rname(self, node, children):
        """The Rnum on any relationship"""
        return {"rnum": children[0]}

    def visit_superclass(self, node, children):
        """Superclass in a generalization relationship"""
        return children[0]

    def visit_subclass(self, node, children):
        """Subclass in a generalization relationship"""
        return children[0]

    def visit_gen_rel(self, node, children):
        """Generalization relationship"""
        return {"superclass": children[0], "subclasses": children[1:]}

    def visit_binary_rel(self, node, children):
        """Binary relationship with or without an association class"""
        items = {k: v for d in children for k, v in d.items()}
        return items

    def visit_rel(self, node, children):
        """Relationship rnum and rel data"""
        return {**children[0], **children[1]}

    def visit_method_block(self, node, children):
        """Methods (unparsed)"""
        # TODO: Parse these eventually
        return {"methods": children}

    def visit_navigation(self, node, children):
        """A reference for a attribute defined as a navigation (only valid if it is unambiguous)"""
        nav_data = {'ref_name'if node == 'attr_ref_name' else
                    node if node != 'class_name' else 'class':
            value[0] if node != 'class_name' else value[0]['name']
            for node, value in children.results.items()} 
        return [('nav_rnum', nav_data, True), ('rnum', children.results['rnum'][0], True)]
        
    def visit_relrnum(self, node, children):
        """Relation as it appear in a reference for a attribute"""
        rnum = children.results['rnum'][0]
        out = [('rnum', rnum, True)]
        if 'union' in children.results:
            out.append(('union_rnum', rnum, True))
        if 'attr_ref_name' in children.results:
            out.append(('ref_name', (rnum, children.results['attr_ref_name'][0]), True))
        return out
    
    def visit_id(self, node, children):
        """id: I, I2, I3"""
        return ('id', node.value, True)

    def visit_attr_name(self, node, children):
        """Attribute name"""
        return ('name', ''.join(children))

    def visit_attr_ref_name(self, node, children):
        """Name of referred attribute"""
        return ''.join(children)
    
    def visit_type_name(self, node, children):
        """Type name"""
        return ('type', ''.join(children))

    def visit_attr(self, node, children):
        """Attribute inside a class"""
        out = dict()
        data_list = [i for child in children for i in (child if type(child) is list else [child])]
        for data in data_list:
            (key, value, *pack) = data
            if not pack:
                out[key] = value
            else: 
                if key not in out:
                    out[key] = list()
                out[key].append(value)
        return out

    def visit_attr_block(self, node, children):
        """Attribute text (unparsed)"""
        return {"attributes": children}

    def visit_class_set(self, node, children):
        """All of the classes"""
        return children

    def visit_class_block(self, node, children):
        """A complete class with attributes, methods, state model"""
        # TODO: No state models yet
        class_attrs = children[0] | children[1]
        block = class_attrs if len(children) == 2 else class_attrs | children[2]
        return block

    def visit_rel_section(self, node, children):
        """Relationships section with all of the relationships"""
        return children

    # Metadata
    def visit_text_item(self, node, children):
        return children[0], False  # Item, Not a resource

    def visit_resource_item(self, node, children):
        return ''.join(children), True  # Item, Is a resource

    def visit_item_name(self, node, children):
        return ''.join(children)

    def visit_data_item(self, node, children):
        return { children[0]: children[1] }

    def visit_metadata(self, node, children):
        """Meta data section"""
        items = {k: v for c in children for k, v in c.items()}
        return items

    # Root
    def visit_subsystem(self, node, children):
        """The complete subsystem"""
        return children


