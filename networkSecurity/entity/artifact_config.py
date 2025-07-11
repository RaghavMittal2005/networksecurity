from dataclasses import dataclass

@dataclass
class IngestionPara:
    training_path:str
    testing_path:str


@dataclass
class DataValidationArtifact:
    validation_status:bool
    valid_train_path:str
    invalid_train_path:str
    invalid_test_path:str
    valid_test_path:str
    drift_report_path:str

@dataclass
class DataTransformationArtifact:
    transformed_train_path:str
    transformed_test_path:str
    transformed_object_path:str