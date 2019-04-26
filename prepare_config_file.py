def edit_config_file_mobilenet_V1(path_to_file, path_to_new_config, number_of_classes=1):
    with open(path_to_file, "r") as config:
        updated_config = config.read().replace("$CLASSES$", str(number_of_classes))

    with open(path_to_new_config, "w") as new_config:
        new_config.write(updated_config)
