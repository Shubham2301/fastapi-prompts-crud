class PromptNotFoundException(Exception):
    def __init__(self, prompt_id: int):
        self.prompt_id = prompt_id

        super().__init__(
            f"Prompt with id {prompt_id} was not found"
        )


class PromptAlreadyExistsException(Exception):
    def __init__(self, prompt_title: str):
        self.prompt_title = prompt_title

        super().__init__(
            f"Prompt with title {prompt_title} already exists"
        )