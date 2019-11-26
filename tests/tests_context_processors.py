from forge.context_processors import debug_features


def test_debug_features(rf, settings):  # pylint: disable=invalid-name
    request = rf.get('/')
    settings.DEBUG = True
    assert debug_features(request)['LOAD_DEBUG_FEATURES']
    settings.DEBUG = False
    assert not debug_features(request)['LOAD_DEBUG_FEATURES']
