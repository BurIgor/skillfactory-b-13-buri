class Tag:
    def __init__(self, tag, klass=None, is_single=False, **kwargs):
        self.tag = tag
        self.is_single = is_single
        self.children = []
        self.text = ""
        self.attributes = {}

        if klass is not None:
            self.attributes["class"] = " ".join(klass)

        for attr, value in kwargs.items():
            self.attributes[attr.replace('_', '-')] = value

    def __iadd__(self, other):
        self.children.append(other)
        return self

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        pass

    def __str__(self):
        attrs = []
        for attribute, value in self.attributes.items():
            attrs.append('%s="%s"' % (attribute, value))
        attrs = " ".join(attrs)

        if self.children:
            opening = '\n<{tag} {attrs}>'.format(tag=self.tag, attrs=attrs)
            if self.text:
                internal = '%s' % self.text
            else:
                internal = ''

            for child in self.children:
                internal += str(child)
            ending = '</%s>' % self.tag
            return opening + internal + ending
        else:
            if self.is_single:
                return '\n<{tag} {attrs}>\n'.format(tag=self.tag, attrs=attrs)
            else:
                return '\n<{tag} {attrs}>{text}</{tag}>'.format(tag=self.tag, attrs=attrs, text=self.text)

class HTML:
    def __init__(self, output=None):
        self.output = output
        self.tag = 'html'
        self.children = []

    def __iadd__(self, other):
        self.children.append(other)
        return self

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.output is not None:
            with open(self.output, 'w') as fp:
                fp.write(str(self))

    def __str__(self):
        opening = '<%s>' % self.tag
        internal = ''
        for child in self.children:
            internal += str(child)
        ending = '\n</%s>' % self.tag
        return opening + internal + ending

class TopLevelTag:
    def __init__(self, tag):
        self.tag = tag
        self.children = []

    def __iadd__(self, other):
        self.children.append(other)
        return self

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def __str__(self):
        opening = '\n<%s>' % self.tag
        internal = ''
        for child in self.children:
            internal += str(child)
        ending = '\n</%s>' % self.tag
        return opening + internal + ending

if __name__ == "__main__":
    with HTML(output=None) as doc:
        with TopLevelTag("head") as head:
            with Tag("title") as title:
                title.text = "hello"
                head += title
            doc += head

        with TopLevelTag("body") as body:
            with Tag("h1", klass=("main-text",)) as h1:
                h1.text = "Test"
                body += h1

            with Tag("div", klass=("container", "container-fluid"), id="lead") as div:
                with Tag("p") as paragraph:
                    paragraph.text = "another test"
                    div += paragraph

                with Tag("img", is_single=True, src="/icon.png") as img:
                    div += img

                body += div

            doc += body

        print(doc)
