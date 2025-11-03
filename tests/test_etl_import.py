def test_import_modules():
    # Prüft nur, dass die Module importierbar sind
    import etl.config as cfg
    import etl.etl as etl_main
    assert hasattr(cfg, "CSV_PATH")
    assert callable(getattr(etl_main, "main", None))
