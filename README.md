ADD TESTS!!!

Configure logging

Campos implementados:

    ============= =================== ========================
    Tipo de campo Campo Django        Widget
    ============= =================== ========================
    text          CharField           default
    textarea      CharField           Textarea
    email         EmailField          default
    radio         ChoiceField         RadioSelect
    select        ChoiceField         default
    multiselect   MultipleChoiceField default
    date          DateField           default with custom type
    datetime      DateTimeField       default with custom type
    duration      DurationField       default
    time          TimeField           default with custom type
    integer       IntegerField        default
    decimal       DecimalField        default
    file          FileField           default
    filepath      FilePathField       default
    image         ImageField          default
    checkbox      BooleanField        CheckboxInput
    ============= =================== =========================

Campos pendientes:

    ============= ========================== =============
    Tipo de campo Campo Django                Widget
    ============= ========================== =============
                  TypedChoiceField
                  FloatField
                  GenericIPAddressField
                  TypedMultipleChoiceField
                  NullBooleanField
                  RegexField
                  SlugField
                  URLField
                  UUIDField
    ============= ========================== =============
