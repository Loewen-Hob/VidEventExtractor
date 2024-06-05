class BaseEvent(object):
    def __init__(self, fields, event_name='Event', key_fields=(), recguid=None):
        self.recguid = recguid
        self.name = event_name
        self.fields = list(fields)
        self.field2content = {f: None for f in fields}
        self.nonempty_count = 0
        self.nonempty_ratio = self.nonempty_count / len(self.fields)

        self.key_fields = set(key_fields)
        for key_field in self.key_fields:
            assert key_field in self.field2content

    def __repr__(self):
        event_str = "\n{}[\n".format(self.name)
        event_str += "  {}={}\n".format("recguid", self.recguid)
        event_str += "  {}={}\n".format("nonempty_count", self.nonempty_count)
        event_str += "  {}={:.3f}\n".format("nonempty_ratio", self.nonempty_ratio)
        event_str += "] (\n"
        for field in self.fields:
            if field in self.key_fields:
                key_str = " (key)"
            else:
                key_str = ""
            event_str += "  " + field + "=" + str(self.field2content[field]) + ", {}\n".format(key_str)
        event_str += ")\n"
        return event_str

    def update_by_dict(self, field2text, recguid=None):
        self.nonempty_count = 0
        self.recguid = recguid

        for field in self.fields:
            if field in field2text and field2text[field] is not None:
                self.nonempty_count += 1
                self.field2content[field] = field2text[field]
            else:
                self.field2content[field] = None

        self.nonempty_ratio = self.nonempty_count / len(self.fields)

    def field_to_dict(self):
        return dict(self.field2content)

    def set_key_fields(self, key_fields):
        self.key_fields = set(key_fields)

    def is_key_complete(self):
        for key_field in self.key_fields:
            if self.field2content[key_field] is None:
                return False

        return True

    def is_good_candidate(self):
        raise NotImplementedError()

    def get_argument_tuple(self):
        args_tuple = tuple(self.field2content[field] for field in self.fields)
        return args_tuple

class FalseAdvertisingEvent(BaseEvent):
    NAME = 'False_Advertising'
    FIELDS = [
        'TIME',
        'LOCATION',
        'AMOUNT',
        'REGULATORY_ORG',
        'PRODUCT_NAME',
        'PRODUCT_BRAND',
        'INVOLVED_COMPANY',
    ]

    def __init__(self, recguid=None):
        super().__init__(
            FalseAdvertisingEvent.FIELDS, event_name=FalseAdvertisingEvent.NAME, recguid=recguid
        )
        self.set_key_fields([
            'TIME',
            'LOCATION',
            'PRODUCT_NAME',
        ])

    def is_good_candidate(self, min_match_count=4):
        key_flag = self.is_key_complete()
        if key_flag:
            if self.nonempty_count >= min_match_count:
                return True
        return False

class CounterfeitingEvent(BaseEvent):
    NAME = 'Counterfeiting'
    FIELDS = [
        'TIME',
        'LOCATION',
        'AMOUNT',
        'REGULATORY_ORG',
        'PRODUCT_NAME',
        'PRODUCT_BRAND',
        'INVOLVED_COMPANY',
        'COUNTERFEIT_QUANTITY',
    ]

    def __init__(self, recguid=None):
        super().__init__(
            CounterfeitingEvent.FIELDS, event_name=CounterfeitingEvent.NAME, recguid=recguid
        )
        self.set_key_fields([
            'TIME',
            'LOCATION',
            'PRODUCT_NAME',
            'COUNTERFEIT_QUANTITY',
        ])

    def is_good_candidate(self, min_match_count=5):
        key_flag = self.is_key_complete()
        if key_flag:
            if self.nonempty_count >= min_match_count:
                return True
        return False

class BANEvent(BaseEvent):
    NAME = 'Ban'
    FIELDS = [
        'TIME',
        'LOCATION',
        'AMOUNT',
        'REGULATORY_ORG',
        'PRODUCT_NAME',
        'PRODUCT_BRAND',
        'INVOLVED_COMPANY',
        'BANNED_SUBSTANCE',
    ]

    def __init__(self, recguid=None):
        super().__init__(
            BANEvent.FIELDS, event_name=BANEvent.NAME, recguid=recguid
        )
        self.set_key_fields([
            'TIME',
            'LOCATION',
            'PRODUCT_NAME',
            'BANNED_SUBSTANCE',
        ])

    def is_good_candidate(self, min_match_count=5):
        key_flag = self.is_key_complete()
        if key_flag:
            if self.nonempty_count >= min_match_count:
                return True
        return False

class NotConformingEvent(BaseEvent):
    NAME = 'Not_Conforming'
    FIELDS = [
        'TIME',
        'LOCATION',
        'AMOUNT',
        'REGULATORY_ORG',
        'PRODUCT_NAME',
        'PRODUCT_BRAND',
        'INVOLVED_COMPANY',
        'NON_COMPLIANCE_REASON',
    ]

    def __init__(self, recguid=None):
        super().__init__(
            NotConformingEvent.FIELDS, event_name=NotConformingEvent.NAME, recguid=recguid
        )
        self.set_key_fields([
            'TIME',
            'LOCATION',
            'PRODUCT_NAME',
            'NON_COMPLIANCE_REASON',
        ])

    def is_good_candidate(self, min_match_count=5):
        key_flag = self.is_key_complete()
        if key_flag:
            if self.nonempty_count >= min_match_count:
                return True
        return False

common_fields = ['TIME', 'LOCATION', 'AMOUNT', 'REGULATORY_ORG', 'PRODUCT_NAME', 'PRODUCT_BRAND', 'INVOLVED_COMPANY']

event_type2event_class = {
    FalseAdvertisingEvent.NAME: FalseAdvertisingEvent,
    CounterfeitingEvent.NAME: CounterfeitingEvent,
    BANEvent.NAME: BANEvent,
    NotConformingEvent.NAME: NotConformingEvent,
}

event_type_fields_list = [
    (FalseAdvertisingEvent.NAME, FalseAdvertisingEvent.FIELDS),
    (CounterfeitingEvent.NAME, CounterfeitingEvent.FIELDS),
    (BANEvent.NAME, BANEvent.FIELDS),
    (NotConformingEvent.NAME, NotConformingEvent.FIELDS),
]
