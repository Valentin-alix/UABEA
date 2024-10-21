from pydantic import Field
from typing_extensions import Annotated

Percentage = Annotated[float, Field(gt=0, le=1)] 
