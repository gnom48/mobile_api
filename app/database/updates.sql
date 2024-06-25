CREATE TYPE public.userkpilevelsorm AS ENUM (
	'TRAINEE',
	'SPECIALIST',
	'EXPERT',
	'TOP');
	
CREATE TABLE last_month_statistics_with_kpi (
    user_id int4 NOT NULL,
    flyers int4 NOT NULL DEFAULT 0,
    calls int4 NOT NULL DEFAULT 0,
    shows int4 NOT NULL DEFAULT 0,
    meets int4 NOT NULL DEFAULT 0,
    deals int4 NOT NULL DEFAULT 0,
    deposits int4 NOT NULL DEFAULT 0,
    searches int4 NOT NULL DEFAULT 0,
    analytics int4 NOT NULL DEFAULT 0,
    others int4 NOT NULL DEFAULT 0,
    user_level public."userkpilevelsorm" not null,
    salary_percentage FLOAT DEFAULT 0.0,
    CONSTRAINT last_month_statistics_with_kpi_pkey PRIMARY KEY (user_id),
	CONSTRAINT last_month_statistics_with_kpi_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE
);