import logging
from typing import List, Dict, Optional, Tuple, Callable
from pyspark.sql import DataFrame
from pyspark.sql import SparkSession
from .utility_manager import UtilityManager
from .orchestration_manager import OrchestrationManager
from .upsert_strategy.upsert_handler import UpsertHandler
from .semantic_model_manager import SemanticModelManager
from .data_validation_manager import Validation
from .transformation_manager import TransformationManager
from .file_manager import FileManager
from .delta_table_manager import DeltaTableManager

class LucidUtils:
    """
    Provides utility functions for managing and manipulating data in Lucid Control Framework.

    :param spark: The SparkSession object.
    """

    def __init__(self):
        """
        Initializes the LucidUtils class.

        :param spark: The SparkSession object.
        """

        # Initialize the SparkSession object
        self.spark = SparkSession.builder.getOrCreate()
        
        # Set up logging
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)

        # Initialize the Lucid Support Modules
        self.utility_manager = UtilityManager()
        self.upsert_handler = UpsertHandler(self.spark, self.logger)
        self.orchestration_manager = OrchestrationManager(self.spark, self.logger)
        self.semantic_model_manager = SemanticModelManager(self.spark, self.logger)
        self.validation = Validation(self.spark, self.logger)
        self.dataframe_transformation_manager = TransformationManager(self.spark, self.logger)
        self.file_manager = FileManager(self.spark, self.logger)
        self.table_manager = DeltaTableManager(self.spark, self.logger)

    def get_secret_value_as_user(
            self,
            key_vault_name: str, 
            secret_name: str
        ) -> str:
        """
        Retrieves a secret value from Azure Key Vault.

        :param key_vault_name: The name of the key vault.
        :param secret_name: The name of the secret within the key vault.
        :return: The value of the secret retrieved from Azure Key Vault.

        Example:
        key_vault_name = "my-key-vault
        secret_name = "my-secret"
        secret_value = UtilityManager.get_secret_value_as_user(key_vault_name, secret_name)
        """
        self.logger.info(f"Getting secret value as user")
        return self.utility_manager.get_secret_value_as_user(key_vault_name, secret_name)
    
    def get_secret_value_as_managed_identity(
            self,
            key_vault_name: str, 
            secret_name: str, 
            managed_identity_name: str
        ) -> str:
        """
        Retrieves a secret value from Azure Key Vault.

        :param key_vault_name: The name of the key vault.
        :param secret_name: The name of the secret within the key vault.
        :param managed_identity_name: The name of the managed identity resource to use for secret retrieval.
        :return: The value of the secret retrieved from Azure Key Vault.

        Example:
        key_vault_name = "my-key-vault
        secret_name = "my-secret"
        managed_identity_name = "my-managed-identity"
        secret_value = UtilityManager.get_secret_value_as_managed_identity(key_vault_name, secret_name, managed_identity_name)
        """
        self.logger.info(f"Getting secret value as managed identity.")
        return self.utility_manager.get_secret_value_as_managed_identity(key_vault_name, secret_name, managed_identity_name)
    
    def read_file(
            self, 
            file_path: str, 
            file_format: str = 'csv'
        ) -> DataFrame:
        """
        Reads a file from the storage account.

        :param file_path: The path of the file.
        :param file_format: The format of the file. Can be 'csv', 'json', 'parquet', etc.
        :return: The DataFrame read from the file.

        Raises:
            ValueError: If an invalid file format is provided.
            Exception: If any error occurs during file reading.

        Example:
            file_path = 'abfss://workspaceid.dfs.core.windows.net/data/Files/file1.csv'
            file_format = 'csv'
        """
        self.logger.info(f"Reading file")
        return self.file_manager.read_file(file_path, file_format)
    
    def read_files_concurrently(
            self, 
            file_paths: list, 
            file_format: str = 'csv'
        ) -> list:
        """
        Reads multiple files from the storage account concurrently.

        :param file_paths: A list of file paths.
        :param file_format: The format of the files. Can be 'csv', 'json', 'parquet', etc.
        :return: A list of DataFrames read from the files.

        Raises:
            Exception: If any error occurs during file reading.

        Example:
            file_paths = ['abfss://workspaceid.dfs.core.windows.net/data/Files/file1.csv', 'abfss://workspaceid.dfs.core.windows.net/data/Files/file2.csv']
            file_format = 'csv'
        """
        self.logger.info(f"Reading files concurrently")
        return self.file_manager.read_files_concurrently(file_paths, file_format)
    
    def write_file(
            self, 
            dataframe: DataFrame, 
            file_name: str, 
            storage_container_endpoint: str, 
            file_format: str = 'parquet'
        ):
        """
        Writes a DataFrame to a file in the storage account.

        :param dataframe: The DataFrame to write.
        :param file_name: The name of the file to write.
        :param storage_container_endpoint: The endpoint of the storage container.
        :param file_format: The format of the file. Can be 'csv', 'json', 'parquet', etc.

        Raises:
            Exception: If any error occurs during file writing.
        
        Example:
            dataframe = df_data
            file_names = 'file1.parquet'
            storage_container_endpoint = 'abfss://workspaceid@onelake.dfs.fabric.microsoft.com/lakehouseid'
            storage_container_endpoint = 'abfss://workspaceid.dfs.core.windows.net/data'
            file_format = 'parquet'
        """
        self.logger.info(f"Writing file")
        return self.file_manager.write_file(dataframe, file_name, storage_container_endpoint, file_format)

    def write_files_concurrently(
            self, 
            dataframe_list: List[DataFrame], 
            file_names: List[str], 
            storage_container_endpoint: str, 
            file_format: str = 'parquet'
        ):
        """
        Writes multiple DataFrames to files in the storage account concurrently.

        :param dataframe_list: A list of DataFrames to write.
        :param file_names: A list of file names.
        :param storage_container_endpoint: The storage container endpoint.
        :param file_format: The format of the files. Can be 'csv', 'json', 'parquet', etc.

        :return: None. The function writes the DataFrames to files.

        Raises:
            ValueError: If the lengths of dataframe_list and file_names do not match.
            Exception: If any error occurs during file writing.

        Example:
            dataframe_list = [spark.createDataFrame([(1, "John", "Doe"), (2, "Jane", "Doe")], ["ID", "First Name", "Last Name"]),
                            spark.createDataFrame([(3, "Jim", "Smith"), (4, "Jill", "Smith")], ["ID", "First Name", "Last Name"])]
            file_names = ['file1.parquet', 'file2.parquet']
            storage_container_endpoint = 'abfss://workspaceid@onelake.dfs.fabric.microsoft.com/lakehouseid'
            storage_container_endpoint = 'abfss://workspaceid.dfs.core.windows.net/data'
            file_format = 'parquet'
            write_files_concurrently(dataframe_list, file_names, storage_container_endpoint, file_format)
        """
        self.logger.info(f"Writing files concurrently")
        return self.file_manager.write_files_concurrently(dataframe_list, file_names, storage_container_endpoint, file_format)
    
    def read_delta_table(
            self, 
            table_name: str, 
            storage_container_endpoint: Optional[str] = None, 
            read_method: str = 'catalog'
        ) -> DataFrame:
        """
        Reads a Delta table into a DataFrame.

        :param table_name: The name of the Delta table.
        :param storage_container_endpoint: The storage container endpoint. Required if read_method is 'path'.
        :param read_method: The method to use for reading the table. Can be either 'path' or 'catalog'.
        :return: The DataFrame representing the Delta table.

        :raises Exception: If there's a problem reading the Delta table.
        :raises ValueError: If an invalid read_method is provided.

        Example:
            table_name = 'my_table'
            storage_container_endpoint = 'abfss://workspaceid@onelake.dfs.fabric.microsoft.com/lakehouseid'
            storage_container_endpoint = 'abfss://workspaceid.dfs.core.windows.net/data'
            read_method = 'default'
            df = delta_table_reader.read_delta_table(table_name, storage_container_endpoint, read_method)
        """
        self.logger.info(f"Reading Delta table")
        return self.table_manager.read_delta_table(table_name, storage_container_endpoint, read_method)
    
    def read_delta_tables_concurrently(
            self, 
            table_names: List[str], 
            storage_container_endpoint: Optional[str] = None, 
            read_method: str = 'catalog'
        ) -> Dict[str, DataFrame]:
        """
        Reads multiple Delta tables into DataFrames concurrently.

        :param table_names: A list of Delta table names.
        :param storage_container_endpoint: The storage container endpoint. Required if read_method is 'path'.
        :param read_method: The method to use for reading the table. Can be either 'path' or 'catalog'.
        :return: A dictionary mapping table names to DataFrames.

        :raises Exception: If there's a problem reading the Delta tables.

        Example:
            table_names = ['table1', 'table2']
            storage_container_endpoint = 'abfss://workspaceid@onelake.dfs.fabric.microsoft.com/lakehouseid'
            storage_container_endpoint = 'abfss://workspaceid.dfs.core.windows.net/data'
            read_method = 'path'
            df_tables = delta_table_reader.read_delta_tables_concurrently(table_names, storage_container_endpoint, read_method)
        """
        self.logger.info(f"Reading Delta tables concurrently")
        return self.table_manager.read_delta_tables_concurrently(table_names, storage_container_endpoint, read_method)
    
    def write_delta_table(
            self, 
            dataframe: DataFrame, 
            table_name: str, 
            storage_container_endpoint: Optional[str] = None, 
            write_method: str = 'catalog', 
            write_mode: str = 'overwrite', 
            merge_schema: str = 'true'
        ) -> None:
        """
        Writes a DataFrame to a Delta table.

        :param dataframe: The DataFrame to write.
        :param table_name: The name of the Delta table.
        :param storage_container_endpoint: The storage container endpoint. Required if write_method is 'path'.
        :param write_method: The method to use for writing the table. Can be either 'path' or 'catalog'.
        :param write_mode: The mode to use for writing the table. Can be 'overwrite', 'append', 'ignore', 'error', or 'overwritePartitions'. Default is 'overwrite'.
        :param merge_schema: Whether to merge the schema of the DataFrame with the schema of the Delta table. Default is 'true'.

        :raises Exception: If there's a problem writing the Delta table.
        :raises ValueError: If an invalid write_method is provided.

        Example:
            dataframe = df_data
            table_name = 'my_table'
            storage_container_endpoint = 'abfss://workspaceid.dfs.core.windows.net/data'
            write_method = 'path'
            write_mode = 'overwrite'
            merge_schema = 'true'
            delta_table_writer.write_delta_table(dataframe, table_name, storage_container_endpoint, write_method)
        """
        self.logger.info(f"Writing Delta table")
        return self.table_manager.write_delta_table(dataframe, table_name, storage_container_endpoint, write_method, write_mode, merge_schema)
    
    def stage_dataframe_with_keys(
            self, 
            target_table: str, 
            dataframe: DataFrame, 
            primary_key_column: Optional[str] = None, 
            composite_key_column: Optional[str] = None, 
            match_key_columns: Optional[List[str]] = None, 
            read_method: str = 'catalog',
            target_table_storage_container_endpoint: Optional[str] = None 
        ) -> Optional[DataFrame]:
        """
        Transforms a DataFrame by adding a new column with an integer hash based on specified key columns.
        It also adds a surrogate key column with values starting from the maximum key in the target table plus one.

        :param target_table: The target table to check for the maximum key.
        :param dataframe: The source DataFrame.
        :param columns: List of column names to include in the transformation.
        :param primary_key_column: The name of the new surrogate key column to be added.
        :param composite_key_column: The name of the new natural key column to be added.
        :param match_key_columns: List of columns to use for hash generation.
        :param read_method: The method to use for reading the target table. Can be either 'path' or 'catalog'.
        :param target_table_storage_container_endpoint: The storage container endpoint for the target table.

        :return: Transformed DataFrame with the new columns added, if specified.

        Example:
            df = spark.createDataFrame([(1, "John", "Doe"), (2, "Jane", "Doe")], ["ID", "First Name", "Last Name"])
            df_transformed = stage_dataframe_with_keys("target_table", df, ["ID", "First Name"], "skey", "nkey", ["ID", "First Name"])
        """
        self.logger.info(f"Staging DataFrame with keys")
        return self.dataframe_transformation_manager.stage_dataframe_with_keys(target_table_storage_container_endpoint, target_table, dataframe, primary_key_column, composite_key_column, match_key_columns, read_method)

    def execute_transformations_concurrently(
            self,
            transformations: List[Tuple[Callable, Tuple]]
    ) -> List:
        """
        Executes multiple DataFrame transformation tasks concurrently, improving performance on multi-core systems.

        :param transformations: A list of tuples, where each tuple contains a transformation function
                                and its corresponding arguments.

        :return: A list of results from each transformation task, executed concurrently.

        Example:
        transformations = [
            (self.stage_dataframe_with_keys, (target_table_storage_container_endpoint1, target_table1, df1, None, None, ["ID", "First Name"])),
            (self.stage_dataframe_with_keys, (target_table_storage_container_endpoint2, target_table2, df2, None, None, ["ID", "First Name"]))
        ]
        results = self.execute_transformations_concurrently(transformations)
        """
        self.logger.info(f"Executing transformations concurrently")
        return self.dataframe_transformation_manager.execute_transformations_concurrently(transformations)

    def upsert_data_concurrently(
            self, 
            table_configs: List[Dict[str, str]], 
            storage_container_endpoint: Optional[str] = None, 
            write_method: str = 'catalog'
        ) -> None:
        """
        Performs upsert operations concurrently on multiple tables based on the provided configurations.

        :param table_configs: A list of table configurations.
        :param storage_container_endpoint: The storage container endpoint (optional).
        :param write_method: The write method (default is 'catalog'). Options are 'catalog' and 'path'.

        Example:
        table_configs = [
            {
                'table_name': 'table1',
                'upsert_type': 'scd2',
                'primary_key': ['id'],
                'composite_columns': ['id', 'name', 'age']
            },
            {
                'table_name': 'table2',
                'upsert_type': 'scd1',
                'primary_key': ['id'],
                'composite_columns': ['id', 'name', 'age']
            }
        ]

        upsert_data_concurrently(table_configs, storage_container_endpoint, write_method)
        """
        self.logger.info(f"Upserting data concurrently")
        return self.upsert_handler.upsert_data_concurrently(table_configs, storage_container_endpoint, write_method)
    
    def log_table_validation(
            self,
            target_table_name: str,
            log_table_name: str,
            read_method: str = 'catalog',
            write_method: str = 'catalog',
            target_storage_container_endpoint: Optional[str] = None,
            log_storage_container_endpoint: Optional[str] = None,
            primary_key_column: Optional[str] = None,
            stage_count: Optional[int] = None,
            invalid_count: Optional[int] = None,
            duplicate_count: Optional[int] = None,
            delete_count: Optional[int] = None
        ) -> None:
        """
        Log the validation results for a table.

        
        :param target_table_name: The name of the target table
        :param log_table_name: The name of the log table
        :param read_method: The method used to read the target table (catalog or path)
        :param write_method: The method used to write the log table (catalog or path)
        :param target_storage_container_endpoint: The storage container endpoint of the target table
        :param log_storage_container_endpoint: The storage container endpoint of the log table
        :param primary_key_column: The primary key column used for filtering
        :param stage_count: The count of rows in the staging DataFrame
        :param invalid_count: Count of invalid records
        :param duplicate_count: Count of duplicate records
        :param delete_count: Count of records flagged for deletion

        Example:
        log_table_validation("storage_container_endpoint", "my_table", "log_storage_container_endpoint", "log_table", "id", 100, 5, 10, 3)
        """
        self.logger.info(f"Logging table validation")
        return self.validation.log_table_validation(target_table_name, log_table_name, read_method, write_method, target_storage_container_endpoint, log_storage_container_endpoint, primary_key_column, stage_count, invalid_count, duplicate_count, delete_count)
    
    def data_validation_check(
            self, 
            df_stage: DataFrame, 
            target_table_name: str,
            target_storage_container_endpoint: str,
            composite_columns: List[str], 
            read_method: str = 'catalog',
            write_method: str = 'catalog',
            primary_key_column: Optional[str] = None, 
            dropped_validation_columns: Optional[List[str]] = None
        ) -> None:
        
        """
        Identify invalid, duplicate, and delete flagged records by identifying them,
        saving them to specified paths, and returning a filtered DataFrame along with counts of invalid, duplicate, and delete flagged records.

        :param df_stage: The staging DataFrame
        :param target_table_name: The name of the table being processed and the target table to check for delete flagged records
        :param target_storage_container_endpoint: The endpoint for the storage account
        :param composite_columns: List of columns to check for invalid values and duplicates and form the composite key
        :param read_method: The method used to read the target table (catalog or path)
        :param write_method: The method used to write the log table (catalog or path)
        :param primary_key_column: The primary key column used for identifying records in the target table
        :param dropped_validation_columns: List of columns to drop from the final DataFrame after validation
        :return: A tuple containing the filtered DataFrame, count of invalid records, count of duplicate records, and count of delete flagged records

        Example:
        data_validation_check(df_stage, "my_table", ["id", "name"], "mydatalake", "id", ["created_at", "updated_at"])
        """
        self.logger.info(f"Starting data validation")
        return self.validation.data_validation_check(df_stage, target_table_name, target_storage_container_endpoint, composite_columns, read_method, write_method, primary_key_column, dropped_validation_columns)
    
    def hard_delete_records(
            self,
            target_table_name: str,
            primary_key_column: str,
            write_method: str = 'catalog',
            target_table_storage_container_endpoint: Optional[str] = None,
            df_delete=None
        ):
        """
        Perform hard deletes from the target table for records identified as delete flagged.

        :param target_table_name: The name of the target table
        :param primary_key_column: The primary key column used for identifying records in the target table
        :param write_method: The method used to write the log table (catalog or path)
        :param target_table_storage_container_endpoint: The storage container endpoint of the target table
        :param df_delete: DataFrame of records flagged for deletion

        Example:
        hard_delete_records('schema.my_table', 'id', 'path', 'target_table_storage_container_endpoint', df_delete)
        """
        self.logger.info(f"Hard deleting records")
        return self.validation.hard_delete_records(target_table_name, primary_key_column, write_method, target_table_storage_container_endpoint, df_delete)
    
    def soft_delete_records(
            self,
            target_table_name: str,
            primary_key_column: str,
            read_method: str = 'catalog',
            target_table_storage_container_endpoint: Optional[str] = None,
            df_delete=None
            ):
        """
        Perform soft deletes from the target table for records identified as delete flagged by setting the is_deleted column to True.
        If the is_deleted column does not exist, it will be added to the target table.

        :param target_table_storage_container_endpoint: The storage container endpoint of the target table
        :param target_table_name: The name of the target table
        :param primary_key_column: The primary key column used for identifying records in the target table
        :param df_delete: DataFrame of records flagged for deletion

        Example:
        soft_delete_records("storage_container_endpoint", "my_table", "id", df_delete)
        """
        self.logger.info(f"Soft deleting records")
        return self.validation.soft_delete_records(target_table_name, primary_key_column, read_method, target_table_storage_container_endpoint, df_delete)
    
    def load_orchestration_config(
            self,
            control_table_name: str,
            orchestration_config: list,
            write_method: str = 'catalog',
            control_storage_container_endpoint: Optional[str] = None
        ):
        """
        Load the orchestration configuration into a DataFrame and save it as a delta table.
        
        :param control_table_name: The name of the control table.
        :param orchestration_config: A list of dictionaries representing the orchestration configuration.
        :param control_storage_container_endpoint: The endpoint of the storage container where the orchestration configuration is stored.

        Example = [
            {
                'notebook_name': 'Notebook1',
                'notebook_path': '/path/to/notebook1',
                'dependencies': '["Notebook2", "Notebook3"]',
                'parameters': '{"param1": "value1", "param2": "value2"}',
                'timeout_per_cell_seconds': 600,
                'retry_attempts': 3,
                'interval_between_retry_attempt_seconds': 60,
                'active': 1,
                'process_group': 1
            },
            {
                'notebook_name': 'Notebook2',
                'notebook_path': '/path/to/notebook2',
                'dependencies': '["Notebook3"]',
                'parameters': '{"param1": "value1", "param2": "value2"}',
                'timeout_per_cell_seconds': 300,
                'retry_attempts': 2,
                'interval_between_retry_attempt_seconds': 30,
                'active': 1,
                'process_group': 1
            }
        ]
        """
        self.logger.info(f"Loading orchestration configuration")
        return self.orchestration_manager.load_orchestration_config(control_table_name, orchestration_config, write_method, control_storage_container_endpoint)
    
    def build_dag(
            self,
            control_table_name: str,
            process_group: int,
            write_method: str = 'catalog',
            control_storage_container_endpoint: Optional[str] = None,
        ) -> dict:
        """
        Build a Directed Acyclic Graph (DAG) for data processing based on the orchestration configuration.
        
        :param control_table_name: The name of the control table.
        :param process_group: The process group to use for building the DAG.
        :param write_method: The method to use for writing the table. Can be either 'path' or 'catalog'.
        :param control_storage_container_endpoint: The endpoint of the storage container where the orchestration configuration is stored.
        :return: A dictionary representing the DAG.

        Example:
        process_group = 1
        dag = OrchestrationManager.build_dag(control_storage_container_endpoint, process_group)
        """
        self.logger.info(f"Building DAG")
        return self.orchestration_manager.build_dag(control_table_name, process_group, write_method, control_storage_container_endpoint)
    
    def log_orchestration_execution(
            self,
            log_table_name: str,
            execution_results: dict,
            write_method: str = 'catalog',
            control_storage_container_endpoint: Optional[str] = None,
        ):
        """
        Log the execution results into a DataFrame and save it as a delta table.
        
        :param log_table_name: The name of the control table.
        :param execution_results: A dictionary representing the execution results.
        :param write_method: The method to use for writing the table. Can be either 'path' or 'catalog'.
        :param control_storage_container_endpoint: The endpoint of the storage container where the orchestration log is stored.

        Example:
        log_orchestration_execution(control_storage_container_endpoint, log_table_name, execution_results)
        """
        self.logger.info(f"Logging orchestration execution")
        return self.orchestration_manager.log_orchestration_execution(log_table_name, execution_results, write_method, control_storage_container_endpoint)
    
    def get_service_principal_pbi_scope_token(
            self, tenant_id: str,
            key_vault_name: str,
            client_id: str,
            client_secret: str,
            managed_identity: str
        ) -> str:
        """
        Retrieves an access token for a service principal using the Microsoft Authentication Library (MSAL).

        :param tenant_id: The Azure Active Directory tenant GUID.
        :param key_vault_name: The name of the Azure Key Vault containing the client ID and client secret.
        :param client_id: The name of the secret containing the client ID in Azure Key Vault.
        :param client_secret: The name of the secret containing the client secret in Azure Key Vault.
        :param managed_identity: The name of the linked service to use for secret retrieval.
        :return: The access token for the service principal.

        Example:
        get_secret_value_as_managed_identity("my-key-vault", "my-client-id", "my-managed-identity")
        """
        self.logger.info(f"Getting service principal PBI scope token")
        return self.semantic_model_manager.get_service_principal_pbi_scope_token(tenant_id, key_vault_name, client_id, client_secret, managed_identity)
    
    def trigger_semantic_model_refresh(
            self, workspace_id: str,
            semantic_model_id: str,
            refresh_token: str
        ) -> None:
        """
        Triggers a refresh of a Power BI dataset.

        :param workspace_id: The ID of the Power BI workspace containing the dataset.
        :param semantic_model_id: The ID of the dataset to refresh.
        :param refresh_token: The refresh token for authentication.
        :return: True if the refresh was successful, False otherwise.

        Example:
        trigger_dataset_refresh("my-workspace-id", "my-dataset-id", "my-refresh-token")
        """
        self.logger.info(f"Triggering semantic model refresh")
        return self.semantic_model_manager.trigger_semantic_model_refresh(workspace_id, semantic_model_id, refresh_token)
    
    def get_semantic_model_refresh_status(
            self, workspace_id: str,
            semantic_model_id: str,
            refresh_token: str
        ) -> None:
        """
        Retrieves the refresh status of a Power BI dataset.

        :param workspace_id: The ID of the Power BI workspace containing the dataset.
        :param semantic_model_id: The ID of the dataset to refresh.
        :param refresh_token: The refresh token for authentication.
        :return: The refresh status of the dataset.

        Example:
        get_dataset_refresh_status("my-workspace-id", "my-dataset-id", "my-refresh-token")
        """
        self.logger.info(f"Getting semantic model refresh status")
        return self.semantic_model_manager.get_semantic_model_refresh_status(workspace_id, semantic_model_id, refresh_token)
    
    def log_semantic_model_refresh_activity(
            self,
            log_table_name: str,
            refresh_state: Dict,
            write_method: str = 'catalog',
            log_table_storage_container_endpoint: Optional[str] = None,
        ) -> None:
        """
        Logs the refresh activity of a Power BI dataset.

        :param log_table_name: The name of the log table in the Azure Storage container.
        :param refresh_state: The refresh state of the dataset.
        :param write_method: The method to use for writing the log table. Can be either 'path' or 'catalog'. Default is 'catalog'.
        :param log_table_storage_container_endpoint: The endpoint of the Azure Storage container where the log table is stored.

        Example:
        log_dataset_refresh_activity(refresh_state)
        """
        self.logger.info(f"Logging semantic model refresh activity")
        return self.semantic_model_manager.log_semantic_model_refresh_activity(log_table_name, refresh_state, write_method, log_table_storage_container_endpoint)