


from abc import ABC, abstractmethod


class Document(ABC):
    """
    Рассмотрим систему обработки документов, где документы могут иметь разные 
    статусы: "черновик", "на рассмотрении", "утвержден", "отклонен".
    """
    def __init__(self, title, content):
        self.title = title
        self.content = content
    
    @abstractmethod
    def process(self):
        pass
    
    @abstractmethod
    def can_edit(self):
        pass
    
    @abstractmethod
    def get_next_actions(self):
        pass
    
    def get_info(self):
        return f"Документ: {self.title}"

class DraftDocument(Document):
    def process(self):
        return "Можно редактировать документ"
    
    def can_edit(self):
        return True
    
    def get_next_actions(self):
        return ["редактировать", "отправить на рассмотрение"]
    
    def save_draft(self):
        return "Черновик сохранен"

class ReviewDocument(Document):
    def __init__(self, title, content, reviewer):
        super().__init__(title, content)
        self.reviewer = reviewer
    
    def process(self):
        return "Документ отправлен на проверку"
    
    def can_edit(self):
        return False
    
    def get_next_actions(self):
        return ["утвердить", "отклонить"]
    
    def assign_reviewer(self, reviewer):
        self.reviewer = reviewer
        return f"Документ назначен на проверку: {reviewer}"

class ApprovedDocument(Document):
    def __init__(self, title, content, approved_by):
        super().__init__(title, content)
        self.approved_by = approved_by
        self.approval_date = "2025-07-23"
    
    def process(self):
        return "Документ утвержден и готов к публикации"
    
    def can_edit(self):
        return False
    
    def get_next_actions(self):
        return ["опубликовать", "архивировать"]
    
    def publish(self):
        return f"Документ опубликован (утвержден: {self.approved_by})"

class RejectedDocument(Document):
    def __init__(self, title, content, rejection_reason):
        super().__init__(title, content)
        self.rejection_reason = rejection_reason
    
    def process(self):
        return "Документ отклонен, требуются исправления"
    
    def can_edit(self):
        return True
    
    def get_next_actions(self):
        return ["исправить", "удалить"]
    
    def get_rejection_details(self):
        return f"Причина отклонения: {self.rejection_reason}"


# Создание документов разных типов
documents = [
    DraftDocument("Техническое задание", "ТЗ для проекта"),
    ReviewDocument("Отчет о работе", "Месячный отчет", "Иванов И.И."),
    ApprovedDocument("Политика безопасности", "Правила безопасности", "Петров П.П."),
    RejectedDocument("Бюджет проекта", "Смета расходов", "Превышен лимит")
]

# Полиморфная обработка
def process_documents(docs):
    for doc in docs:
        print(f"\n{doc.get_info()}")
        print(f"Статус: {doc.process()}")
        print(f"Можно редактировать: {doc.can_edit()}")
        print(f"Доступные действия: {', '.join(doc.get_next_actions())}")
        
        # Специфические методы для каждого типа
        if isinstance(doc, ReviewDocument):
            print(f"Проверяющий: {doc.reviewer}")
        elif isinstance(doc, ApprovedDocument):
            print(f"Утвержден: {doc.approved_by}")
        elif isinstance(doc, RejectedDocument):
            print(doc.get_rejection_details())

process_documents(documents)
