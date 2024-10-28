import re

class RegexUtils:
    MORE_THAN_ONE_FOUND = "More than one match found"
    ZERO_FOUND = "No match was found"
    @classmethod
    def retrieve_regex_between(cls, data, header, footer):
        pattern = re.compile(r'^(' + header + r')((?:\s|.)*?)^(' + footer + r')$', re.MULTILINE)
        matches = re.findall(pattern, data)
        assert len(matches) <= 1, cls.MORE_THAN_ONE_FOUND
        assert len(matches) >= 1, "No match was found"
        match = matches[0]
        header = match[0]
        body = match[1]
        footer = match[2]
        
        return header, body, footer

    @classmethod
    def retrieve_re_section(cls, data, header, level):
        footer = r'\ {0,' + str(level) + r'}\S.*'
        return cls.retrieve_regex_between(data, header, footer)

    @classmethod
    def retrieve_section(cls, data, exact_header, level):
        level = int(level)
        exact_header= str(exact_header)
        header = re.escape(" " * level + exact_header) + r"\n"
        return cls.retrieve_re_section(data, header, level)

    @classmethod
    def get_sparse_order(cls, data, elements):
        pattern_str = "(?:(.|\n)*)".join(map(
            lambda element: "^ *(" + re.escape(element) + ") *$",
            elements
            )
        )
        print("((?:.|\n)*)" + pattern_str + "((?:.|\n)*)")
        pattern = re.compile("((?:.|\n)*)" + pattern_str + "((?:.|\n)*)", re.MULTILINE)

        matches = re.findall(pattern, data)

        print(len(matches))
        assert len(matches) <= 1, cls.MORE_THAN_ONE_FOUND
        assert len(matches) >= 1, cls.ZERO_FOUND

        return list(matches[0])

    @classmethod
    def findall_groupings(cls, data, pattern_str):
        pattern = re.compile(pattern_str, re.MULTILINE)
        matches = re.findall(pattern, data)

        assert len(matches) <= 1, cls.MORE_THAN_ONE_FOUND
        assert len(matches) >= 1, cls.ZERO_FOUND

        return list(matches[0])


# data = """
# vrf definition TEST_VPN_BASE_IPv4_001
# rd 123:97
# !
# address-family ipv4
# route-target export 123:7
# maximum routes 100 80
# exit-address-family
# !
# """
#
#
# target = "vrf definition TEST_VPN_BASE_IPv4_001"
#
# op = RegexUtils.get_sparse_order(data, target)
# print(op)