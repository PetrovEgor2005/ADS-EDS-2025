erDiagram
    USERS {
        uuid id PK
        bigint telegram_id "UNIQUE"
        varchar username
        varchar role "admin|recruiter|seeker"
        timestamptz created_at
    }

    COMPANIES {
        uuid id PK
        varchar name "UNIQUE"
        boolean is_active
        timestamptz created_at
    }

    RECRUITERS {
        uuid id PK
        uuid user_id "FK -> USERS.id (UNIQUE)"
        boolean is_approved
        timestamptz created_at
    }

    CANDIDATES {
        uuid id PK
        uuid user_id "FK -> USERS.id (UNIQUE)"
        varchar full_name
        varchar city
        uuid current_company_id "FK -> COMPANIES.id (NULLABLE)"
        boolean hide_from_current_company
        timestamptz created_at
    }

    RECRUITER_COMPANIES {
        uuid recruiter_id "FK -> RECRUITERS.id"
        uuid company_id "FK -> COMPANIES.id"
        timestamptz created_at
    }

    VACANCIES {
        uuid id PK
        uuid company_id "FK -> COMPANIES.id"
        uuid recruiter_id "FK -> RECRUITERS.id"
        varchar title
        text description
        varchar city
        varchar work_format "office|remote|hybrid"
        integer salary_min
        integer salary_max
        varchar currency
        varchar status "open|closed|archived"
        timestamptz created_at
        timestamptz updated_at
    }

    APPLICATIONS {
        uuid id PK
        uuid candidate_id "FK -> CANDIDATES.id"
        uuid vacancy_id "FK -> VACANCIES.id"
        varchar status "applied|viewed|invited|rejected"
        timestamptz created_at
        timestamptz updated_at
    }

    REACTIONS {
        uuid id PK
        uuid candidate_id "FK -> CANDIDATES.id"
        uuid vacancy_id "FK -> VACANCIES.id"
        varchar type "like|dislike|complain"
        timestamptz created_at
    }

    CANDIDATE_COMPANY_BLOCKS {
        uuid candidate_id "FK -> CANDIDATES.id"
        uuid company_id "FK -> COMPANIES.id"
        timestamptz created_at
    }

    USERS ||--o| RECRUITERS : "has recruiter profile"
    USERS ||--o| CANDIDATES : "has candidate profile"

    COMPANIES ||--o{ VACANCIES : "publishes"
    RECRUITERS ||--o{ VACANCIES : "creates"

    RECRUITERS ||--o{ RECRUITER_COMPANIES : "member"
    COMPANIES ||--o{ RECRUITER_COMPANIES : "has recruiters"

    CANDIDATES ||--o{ APPLICATIONS : "submits"
    VACANCIES ||--o{ APPLICATIONS : "receives"

    CANDIDATES ||--o{ REACTIONS : "reacts"
    VACANCIES ||--o{ REACTIONS : "gets reactions"

    CANDIDATES ||--o{ CANDIDATE_COMPANY_BLOCKS : "blocks"
    COMPANIES ||--o{ CANDIDATE_COMPANY_BLOCKS : "is blocked"
