import re
from typing import Optional, List
from pydantic import BaseModel, Field, validator

class Author(BaseModel):
    last_name: Optional[str] = None
    fore_name: Optional[str] = None
    initials: Optional[str] = None
    affiliation: Optional[str] = None

    @property
    def full_name(self) -> str:
        return f"{self.fore_name or ''} {self.last_name or ''}".strip()

class Paper(BaseModel):
    pubmed_id: str = Field(..., alias="PMID")
    title: str
    publication_date: str
    authors: List[Author] = []
    
    # Processed fields will be populated later
    non_academic_authors: List[str] = []
    company_affiliations: List[str] = []
    corresponding_author_email: Optional[str] = None

    @validator('title', pre=True, always=True)
    def clean_title(cls, value):
        # Titles can have weird formatting; this cleans it up
        return ' '.join(str(value).split()) if value else "[No Title]"

    def find_corresponding_email(self):
        """Heuristic to find corresponding author email from affiliations."""
        email_pattern = re.compile(r'[\w\.-]+@[\w\.-]+')
        for author in self.authors:
            if author.affiliation:
                match = email_pattern.search(author.affiliation)
                if match:
                    email = match.group(0)
                    # Often the email is at the end, sometimes with a period.
                    if email.endswith('.'):
                        email = email[:-1]
                    self.corresponding_author_email = email
                    return # Stop after finding the first email