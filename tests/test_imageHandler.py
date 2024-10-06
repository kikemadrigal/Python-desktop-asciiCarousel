def test_get_image():
    from convert2Ascii.imageHandler import get_image
    image = get_image()
    assert image is not None