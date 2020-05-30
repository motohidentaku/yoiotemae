def make_json(measurment, tags, data):
    """
    make json
    Parameters
    ----------
    measurmant : string
        influx measurment
    tasg : string
        influx tags
    data : array
        influx : fields
    Returns
    -------
    json_body : string
        json string
    """
    json_body = [
            {
                "measurement": measurment,
                "tags": tags,
                "fields": data
                }
            ]

    return json_body
