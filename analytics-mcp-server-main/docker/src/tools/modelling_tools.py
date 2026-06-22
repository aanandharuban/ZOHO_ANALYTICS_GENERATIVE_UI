from src.mcp_instance import mcp
from src.config import Settings, get_analytics_client_instance
from src.utils.analytics.common import retry_with_fallback
from src.utils.analytics.modelling import (
    create_workspace_implementation,
    create_table_implementation,
    create_aggregate_formula_implementation,
    # create_chart_report_implementation,
    # create_pivot_report_implementation,
    # create_summary_report_implementation,
    create_query_table_implementation,
    delete_view_implementation,
)
import traceback
from fastmcp.server.dependencies import get_context
from fastmcp.apps.generative import GenerativeUI

mcp.add_provider(GenerativeUI())


@mcp.tool()
async def create_workspace(workspace_name: str, org_id: str | None = None) -> str:
    """
    <use_case>
        Create a new workspace in zoho analytics with the given name.
    </use_case>

    <important_notes>
        A workspace is a container for related zoho analytics objects like tables, reports, and dashboards.
    </important_notes>
    """
    try:
        if not org_id:
            org_id = Settings.ORG_ID
        return await retry_with_fallback(
            [org_id],
            None,
            None,
            create_workspace_implementation,
            workspace_name=workspace_name,
        )
    except Exception as e:
        ctx = get_context()
        await ctx.error(traceback.format_exc())
        error_message = e.message if hasattr(e, "message") else str(e)
        return f"An error occurred while creating the workspace : {error_message}"


@mcp.tool()
async def create_table(
    workspace_id: str,
    table_name: str,
    columns_list: list[dict],
    org_id: str | None = None,
) -> str:
    """
    <use_case>
        Create a new table in the given workspace with the given name.
    </use_case>

    <arguments>
        workspace_id (str): The ID of the workspace in which to create the table.
        table_name (str): The name of the table to create.
        columns_list (list[dict]): A list of dictionaries representing the columns of the table.
            Each dictionary should contain the following keys:
                - "COLUMNNAME": The name of the column.
                - "DATATYPE": The data type of the column ("PLAIN", "NUMBER", "DATE").
        org_id (str | None): The ID of the organization to which the workspace belongs to. If not provided, it defaults to the organization ID from the configuration.
    </arguments>
    """
    try:
        if not org_id:
            org_id = Settings.ORG_ID
        return await retry_with_fallback(
            [org_id],
            workspace_id,
            "WORKSPACE",
            create_table_implementation,
            workspace_id=workspace_id,
            table_name=table_name,
            columns_list=columns_list,
        )
    except Exception as e:
        ctx = get_context()
        await ctx.error(traceback.format_exc())
        error_message = e.message if hasattr(e, "message") else str(e)
        return f"An error occurred while creating the table : {error_message}"


@mcp.tool()
async def create_aggregate_formula(
    workspace_id: str,
    table_id: str,
    expression: str,
    formula_name: str,
    org_id: str | None = None,
) -> str:
    """
    <use_case>
        Create an aggregate formula in the specified table of the workspace.
    </use_case>

    <important_notes>
        1. Aggregate Formulas in zoho analytics are select query expression that returns a single aggregate value as output.
        2. The expression should always return a valid aggregate value.
        3. Any Column or Table names used should be enclosed in double quotes. Literal values should be enclosed in single quotes.
        4. While the expression can contain complex nested functions, it should always return a single aggregate value.
        5. Assume that the expression is mysql compatible.
    </important_notes>

    <arguments>
        1. workspace_id (str): The ID of the workspace.
        2. table_id (str): The ID of the table.
        3. expression (str): The expression for the aggregate formula.
            For example, SUM("Revenue") or AVG("Salary").
            The expression should be a valid SQL aggregate function.
        4. formula_name (str): The name of the aggregate formula.
        5. org_id (str | None): The ID of the organization to which the workspace belongs to. If not provided, it defaults to the organization ID from the configuration.
    </arguments>

    <returns>
        str: The result of the operation. If successful, it returns the ID of the created aggregate formula.
    </returns>
    """
    try:
        if not org_id:
            org_id = Settings.ORG_ID
        return await retry_with_fallback(
            [org_id],
            workspace_id,
            "WORKSPACE",
            create_aggregate_formula_implementation,
            workspace_id=workspace_id,
            table_id=table_id,
            expression=expression,
            formula_name=formula_name,
        )
    except Exception as e:
        ctx = get_context()
        await ctx.error(traceback.format_exc())
        error_message = e.message if hasattr(e, "message") else str(e)
        return (
            f"An error occurred while creating the aggregate formula : {error_message}"
        )


@mcp.tool()
async def create_query_table(
    workspace_id: str, table_name: str, query: str, org_id: str | None = None
) -> str:
    """
    <use_case>
        1. Create a query table in the specified workspace with the given name and SQL query.
        2. Used when user needs to create a derived table based on a SQL query.
        3. Used when further transformations are needed on existing tables.
    </use_case>

    <important_notes>
        1. Query Tables in Zoho Analytics are derived tables created from a SQL query.
        2. The query should be a valid SQL query that returns a result set.
        3. Query tables can be used in charts and other reports just like regular tables.
        4. The query should be a valid MYSQL compatible select query.
    </important_notes>

    <arguments>
        workspace_id (str): The ID of the workspace in which to create the query table.
        table_name (str): The name of the query table to create.
        query (str): The SQL select query to create the query table.
        org_id (str | None): The ID of the organization to which the workspace belongs to. If not provided, it defaults to the organization ID from the configuration.
    </arguments>

    <returns>
        str: The result of the operation. If successful, it returns the ID of the created query table.
    </returns>
    """
    try:
        if not org_id:
            org_id = Settings.ORG_ID
        return await retry_with_fallback(
            [org_id],
            workspace_id,
            "WORKSPACE",
            create_query_table_implementation,
            workspace_id=workspace_id,
            table_name=table_name,
            query=query,
        )
    except Exception as e:
        ctx = get_context()
        await ctx.error(traceback.format_exc())
        error_message = e.message if hasattr(e, "message") else str(e)
        return f"An error occurred while creating the query table : {error_message}"


@mcp.tool()
async def delete_view(
    workspace_id: str, view_id: str, org_id: str | None = None
) -> str:
    """
    <use_case>
        Delete a view (table, report, or dashboard) in the specified workspace.
    </use_case>

    <arguments>
        workspace_id (str): The ID of the workspace containing the view.
        view_id (str): The ID of the view to delete.
        org_id (str | None): The ID of the organization to which the workspace belongs to. If not provided, it defaults to the organization ID from the configuration.
    </arguments>
    """
    try:
        if not org_id:
            org_id = Settings.ORG_ID
        return await retry_with_fallback(
            [org_id],
            workspace_id,
            "WORKSPACE",
            delete_view_implementation,
            workspace_id=workspace_id,
            view_id=view_id,
        )
    except Exception as e:
        ctx = get_context()
        await ctx.error(traceback.format_exc())
        error_message = e.message if hasattr(e, "message") else str(e)
        return f"An error occurred while deleting the view: {error_message}"
