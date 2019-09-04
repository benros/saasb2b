import snowflake.connector


def get_snowflake_cursor(db_config: dict) -> snowflake.connector.cursor:
    """
    Creates and returns a cursor object from a connector object.
    Before returning a cursor, run some USE commands.
    :param db_config: the connection details from the config.ini file
    :return:
    """
    ctx = snowflake.connector.connect(
        user=db_config["user"],
        password=db_config["password"],
        account=db_config["account"]
    )
    run_use_commands(ctx, db_config)
    return ctx.cursor()


def run_use_commands(ctx: snowflake.connector, db_config: dict):
    """
    Runs USE commands by the cursor, for defining the warehouse, database
    and schema. We get errors otherwise. The commands are run in the DB and
    kept for the entire session.
    :param ctx: snowflake.connector object
    :param db_config: the connection details from the config.ini file
    :return: None
    """
    use_commands = f"USE WAREHOUSE \"{db_config['warehouse']}\"; " \
                   f"USE DATABASE \"{db_config['database']}\"; " \
                   f"USE SCHEMA \"{db_config['schema']}\"; "
    ctx.execute_string(use_commands)


def execute_string_as_list_of_dicts(ctx: snowflake.connector,
                                    queries_string: str,
                                    remove_comments: bool = False,
                                    return_cursors: bool = True):
    """
    Executes a string of sql commands and returns a list of dict, where each
    dict is a row from the results.
    :param ctx: Connector to snowflake DB
    :param queries_string: semicolon separated sql commands
    :param remove_comments: whether or not to remove comments from the queries
    :param return_cursors: Whether to return a list of cursors in the order of
                            the queries in queries_string
    :return: list[dict]: the results of the queries in queries_string,
                        as list of dicts
    """
    res_list = ctx.execute_string(sql_text=queries_string,
                                  remove_comments=remove_comments,
                                  return_cursors=return_cursors)
    results_list = []
    for query_idx, res in enumerate(res_list, start=1):
        columns = [col[0] for col in res.description]
        rows = res.fetchall()

        table_list = []

        for row in rows:
            table_list.append(
                {
                    col: row[idx]
                    for idx, col in enumerate(columns)
                })
        results_list.append({f"query_{query_idx}: {table_list}"})

    return results_list
