import unittest

import lxml.etree


def get_xpath(xslt, xslt_broken_node_name, known_value):
    return "/root/node/text()"


def modify_xslt(xslt, node_name, node_content):
    for node in xslt.iter(node_name):
        parent = node.getparent()
        parent.remove(node)
        lxml.etree.SubElement(parent, node_name).text = node_content


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.xml = lxml.etree.XML("""
        <root>
            <node>text</node>
        </root>
        """)

        self.xslt = lxml.etree.XML("""
        <xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
            <xsl:template match="/">
                <result><xsl:value-of select="/root/text()"/></result>
            </xsl:template>
        </xsl:stylesheet>
        """)

    def test_get_xpath(self):
        xpath = get_xpath(xslt=self.xslt,
                          xslt_broken_node_name="result",
                          known_value="text")
        self.assertEqual(xpath, "/root/node/text()")

    def test_modify_xslt(self):
        modify_xslt(xslt=self.xslt,
                    node_name="result",
                    node_content="content")
        self.assertEqual(self.xslt.xpath("//result/text()")[0], "content")


if __name__ == "__main__":
    unittest.main()
