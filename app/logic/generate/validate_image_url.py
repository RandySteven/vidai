from temporalio import activity
from app.logic.generate.execution_data import ExecutionData

@activity.defn
def validate_image_url(execution_data: ExecutionData) -> bool:
    if execution_data.image is None:
        raise Exception("Image is required")
    return True