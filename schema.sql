--
-- PostgreSQL database dump
--

\restrict IWze57H9TprkNaItOne3ETpMZ0wj9Ufj2U4FmR3EKuQf1sEwvkybjMtUsF2ymit

-- Dumped from database version 18.4
-- Dumped by pg_dump version 18.4

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: attendance_logs; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.attendance_logs (
    id integer NOT NULL,
    schedule_id integer NOT NULL,
    student_id integer NOT NULL,
    scan_method character varying(20),
    "timestamp" timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    scanned_by character varying(255),
    checkin_point integer
);


ALTER TABLE public.attendance_logs OWNER TO postgres;

--
-- Name: COLUMN attendance_logs.scan_method; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.attendance_logs.scan_method IS 'วิธีที่ใช้แสกน: face, qr, barcode, manual';


--
-- Name: COLUMN attendance_logs."timestamp"; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.attendance_logs."timestamp" IS 'วัน-เวลาที่สแกนสำเร็จ';


--
-- Name: COLUMN attendance_logs.scanned_by; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.attendance_logs.scanned_by IS 'ชื่อหรือ ID ของเจ้าหน้าที่ผู้สแกน';


--
-- Name: attendance_logs_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.attendance_logs_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.attendance_logs_id_seq OWNER TO postgres;

--
-- Name: attendance_logs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.attendance_logs_id_seq OWNED BY public.attendance_logs.id;


--
-- Name: audit_logs; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.audit_logs (
    log_id integer NOT NULL,
    student_id integer,
    action_type character varying(100) NOT NULL,
    description text,
    ip_address character varying(45),
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.audit_logs OWNER TO postgres;

--
-- Name: audit_logs_log_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.audit_logs_log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.audit_logs_log_id_seq OWNER TO postgres;

--
-- Name: audit_logs_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.audit_logs_log_id_seq OWNED BY public.audit_logs.log_id;


--
-- Name: deliveries; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.deliveries (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    graduation_id uuid NOT NULL,
    shipping_address text NOT NULL,
    shipping_method integer NOT NULL,
    shipping_cost numeric(10,2) NOT NULL,
    payment_status character varying(50) DEFAULT 'pending'::character varying,
    tracking_number character varying(100),
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    shipping_destination character varying(50)
);


ALTER TABLE public.deliveries OWNER TO postgres;

--
-- Name: TABLE deliveries; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.deliveries IS 'ตารางเก็บข้อมูลการจัดส่งปริญญาบัตรทางไปรษณีย์และสถานะการชำระเงิน';


--
-- Name: department; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.department (
    facultyid integer NOT NULL,
    departmentid integer NOT NULL,
    departmentname character varying,
    departmentnameeng character varying
);


ALTER TABLE public.department OWNER TO postgres;

--
-- Name: faculty; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.faculty (
    facultyid integer NOT NULL,
    facultyname character varying NOT NULL,
    facultynameeng character varying
);


ALTER TABLE public.faculty OWNER TO postgres;

--
-- Name: grad_students; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.grad_students (
    id integer CONSTRAINT grad_students_orderno_not_null NOT NULL,
    acadyear integer,
    studentcode character varying(20) NOT NULL,
    birthdate date,
    levelid character varying(10),
    levelname character varying(100),
    levelnameeng character varying(100),
    facultyid character varying(10),
    facultyname character varying(150),
    facultynameeng character varying(150),
    departmentid character varying(10),
    departmentname character varying(150),
    departmentnameeng character varying(150),
    programid character varying(10),
    programname character varying(200),
    programnameeng character varying(200),
    prefixname text,
    prefixnameeng text,
    studentname text,
    studentnameeng text,
    studentsurname text,
    studentsurnameeng text,
    gpax numeric(3,2),
    email character varying(100),
    mobile character varying(20),
    finishdate date,
    current_address text,
    current_village character varying(100),
    current_moo character varying(10),
    current_soi character varying(100),
    current_road character varying(100),
    current_subdistrict character varying(100),
    current_district character varying(100),
    current_zipcode text,
    current_provincename character varying(100),
    current_provincenameeng character varying(100),
    current_phone character varying(20),
    home_address text,
    home_village character varying(100),
    home_moo character varying(10),
    home_soi character varying(100),
    home_road character varying(100),
    home_subdistrict character varying(100),
    home_district character varying(100),
    home_zipcode text,
    home_provincename character varying(100),
    home_provincenameeng character varying(100),
    home_phone character varying(20),
    thaistudent character varying(10),
    bpass character varying(50),
    degreename character varying(150),
    degreenameeng character varying(150),
    debt numeric(10,2) DEFAULT 0.00,
    orderno integer CONSTRAINT grad_students_orderno_not_null1 NOT NULL,
    first_name_read character varying,
    last_name_read character varying
);


ALTER TABLE public.grad_students OWNER TO postgres;

--
-- Name: grad_students_orderno_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.grad_students_orderno_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.grad_students_orderno_seq OWNER TO postgres;

--
-- Name: grad_students_orderno_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.grad_students_orderno_seq OWNED BY public.grad_students.id;


--
-- Name: graduations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.graduations (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    student_id integer NOT NULL,
    is_attending integer,
    food_type character varying(50),
    food_allergy text,
    face_image_url text,
    survey_completed boolean DEFAULT false,
    status character varying(50) DEFAULT 'pending'::character varying,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    pregnancy_month integer,
    reason character varying,
    version integer DEFAULT 1 NOT NULL
);


ALTER TABLE public.graduations OWNER TO postgres;

--
-- Name: TABLE graduations; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.graduations IS 'ตารางเก็บข้อมูลการแจ้งความประสงค์เข้ารับพระราชทานปริญญาบัตร';


--
-- Name: COLUMN graduations.reason; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.graduations.reason IS 'สำหรับใส่เหตุผลการไม่เข้ารับ';


--
-- Name: mst_attendance_type; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mst_attendance_type (
    type_id integer NOT NULL,
    type_name character varying,
    is_attend boolean,
    require_remark character varying
);


ALTER TABLE public.mst_attendance_type OWNER TO postgres;

--
-- Name: TABLE mst_attendance_type; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.mst_attendance_type IS 'master เก็บรหัสการเข้ารับ';


--
-- Name: mst_event_schedules; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mst_event_schedules (
    id integer NOT NULL,
    academic_year character varying(4),
    event_name character varying(255),
    event_date timestamp with time zone,
    session_type character varying(50),
    is_active boolean DEFAULT false
);


ALTER TABLE public.mst_event_schedules OWNER TO postgres;

--
-- Name: COLUMN mst_event_schedules.academic_year; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.mst_event_schedules.academic_year IS 'ปีการศึกษา เช่น 2568';


--
-- Name: COLUMN mst_event_schedules.event_name; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.mst_event_schedules.event_name IS 'ชื่อรอบกิจกรรม เช่น ซ้อมย่อย 1, ซ้อมใหญ่, รับจริง';


--
-- Name: COLUMN mst_event_schedules.session_type; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.mst_event_schedules.session_type IS 'ช่วงเวลา เช่น morning, afternoon';


--
-- Name: COLUMN mst_event_schedules.is_active; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.mst_event_schedules.is_active IS 'สถานะว่ากำลังเปิดให้เช็คชื่อรอบนี้อยู่หรือไม่ (ควรมี True แค่ 1 record ณ เวลานั้น)';


--
-- Name: mst_event_schedules_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.mst_event_schedules_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.mst_event_schedules_id_seq OWNER TO postgres;

--
-- Name: mst_event_schedules_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.mst_event_schedules_id_seq OWNED BY public.mst_event_schedules.id;


--
-- Name: mst_food_type; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mst_food_type (
    food_type_id integer NOT NULL,
    food_type_name character varying(100) NOT NULL,
    is_active boolean DEFAULT true,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.mst_food_type OWNER TO postgres;

--
-- Name: mst_food_type_food_type_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.mst_food_type_food_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.mst_food_type_food_type_id_seq OWNER TO postgres;

--
-- Name: mst_food_type_food_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.mst_food_type_food_type_id_seq OWNED BY public.mst_food_type.food_type_id;


--
-- Name: mst_shipping_method; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mst_shipping_method (
    shipping_method_id integer NOT NULL,
    method_name character varying(255) NOT NULL,
    description text,
    require_remark character varying(50),
    is_active boolean DEFAULT true
);


ALTER TABLE public.mst_shipping_method OWNER TO postgres;

--
-- Name: mst_shipping_rate; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mst_shipping_rate (
    rate_id integer NOT NULL,
    shipping_method_id integer,
    rate_amount numeric(10,2) DEFAULT 0.00 NOT NULL,
    currency character varying(10) DEFAULT 'THB'::character varying,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.mst_shipping_rate OWNER TO postgres;

--
-- Name: mst_shipping_rate_rate_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.mst_shipping_rate_rate_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.mst_shipping_rate_rate_id_seq OWNER TO postgres;

--
-- Name: mst_shipping_rate_rate_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.mst_shipping_rate_rate_id_seq OWNED BY public.mst_shipping_rate.rate_id;


--
-- Name: payment_transactions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.payment_transactions (
    transaction_id integer NOT NULL,
    student_id integer NOT NULL,
    reference_no character varying(100) NOT NULL,
    amount numeric(10,2) NOT NULL,
    payment_status character varying(50) DEFAULT 'pending'::character varying,
    payment_channel character varying(50),
    paid_at timestamp without time zone,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.payment_transactions OWNER TO postgres;

--
-- Name: payment_transactions_transaction_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.payment_transactions_transaction_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.payment_transactions_transaction_id_seq OWNER TO postgres;

--
-- Name: payment_transactions_transaction_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.payment_transactions_transaction_id_seq OWNED BY public.payment_transactions.transaction_id;


--
-- Name: survey_tokens; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.survey_tokens (
    token_id integer NOT NULL,
    student_id integer NOT NULL,
    token_string character varying(255) NOT NULL,
    is_used boolean DEFAULT false,
    expires_at timestamp without time zone,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.survey_tokens OWNER TO postgres;

--
-- Name: survey_tokens_token_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.survey_tokens_token_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.survey_tokens_token_id_seq OWNER TO postgres;

--
-- Name: survey_tokens_token_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.survey_tokens_token_id_seq OWNED BY public.survey_tokens.token_id;


--
-- Name: system_settings; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.system_settings (
    setting_key character varying NOT NULL,
    setting_value character varying,
    description character varying
);


ALTER TABLE public.system_settings OWNER TO postgres;

--
-- Name: attendance_logs id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.attendance_logs ALTER COLUMN id SET DEFAULT nextval('public.attendance_logs_id_seq'::regclass);


--
-- Name: audit_logs log_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.audit_logs ALTER COLUMN log_id SET DEFAULT nextval('public.audit_logs_log_id_seq'::regclass);


--
-- Name: grad_students id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.grad_students ALTER COLUMN id SET DEFAULT nextval('public.grad_students_orderno_seq'::regclass);


--
-- Name: mst_event_schedules id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mst_event_schedules ALTER COLUMN id SET DEFAULT nextval('public.mst_event_schedules_id_seq'::regclass);


--
-- Name: mst_food_type food_type_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mst_food_type ALTER COLUMN food_type_id SET DEFAULT nextval('public.mst_food_type_food_type_id_seq'::regclass);


--
-- Name: mst_shipping_rate rate_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mst_shipping_rate ALTER COLUMN rate_id SET DEFAULT nextval('public.mst_shipping_rate_rate_id_seq'::regclass);


--
-- Name: payment_transactions transaction_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.payment_transactions ALTER COLUMN transaction_id SET DEFAULT nextval('public.payment_transactions_transaction_id_seq'::regclass);


--
-- Name: survey_tokens token_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.survey_tokens ALTER COLUMN token_id SET DEFAULT nextval('public.survey_tokens_token_id_seq'::regclass);


--
-- Name: attendance_logs attendance_logs_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.attendance_logs
    ADD CONSTRAINT attendance_logs_pkey PRIMARY KEY (id);


--
-- Name: audit_logs audit_logs_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.audit_logs
    ADD CONSTRAINT audit_logs_pkey PRIMARY KEY (log_id);


--
-- Name: deliveries deliveries_graduation_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.deliveries
    ADD CONSTRAINT deliveries_graduation_id_key UNIQUE (graduation_id);


--
-- Name: deliveries deliveries_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.deliveries
    ADD CONSTRAINT deliveries_pkey PRIMARY KEY (id);


--
-- Name: department department_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.department
    ADD CONSTRAINT department_pkey PRIMARY KEY (facultyid, departmentid);


--
-- Name: faculty faculty_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.faculty
    ADD CONSTRAINT faculty_pkey PRIMARY KEY (facultyid);


--
-- Name: grad_students grad_students_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.grad_students
    ADD CONSTRAINT grad_students_pkey PRIMARY KEY (id);


--
-- Name: graduations graduations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.graduations
    ADD CONSTRAINT graduations_pkey PRIMARY KEY (id);


--
-- Name: mst_attendance_type mst_attendance_type_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mst_attendance_type
    ADD CONSTRAINT mst_attendance_type_pkey PRIMARY KEY (type_id);


--
-- Name: mst_event_schedules mst_event_schedules_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mst_event_schedules
    ADD CONSTRAINT mst_event_schedules_pkey PRIMARY KEY (id);


--
-- Name: mst_food_type mst_food_type_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mst_food_type
    ADD CONSTRAINT mst_food_type_pkey PRIMARY KEY (food_type_id);


--
-- Name: mst_shipping_method mst_shipping_method_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mst_shipping_method
    ADD CONSTRAINT mst_shipping_method_pkey PRIMARY KEY (shipping_method_id);


--
-- Name: mst_shipping_rate mst_shipping_rate_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mst_shipping_rate
    ADD CONSTRAINT mst_shipping_rate_pkey PRIMARY KEY (rate_id);


--
-- Name: payment_transactions payment_transactions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.payment_transactions
    ADD CONSTRAINT payment_transactions_pkey PRIMARY KEY (transaction_id);


--
-- Name: payment_transactions payment_transactions_reference_no_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.payment_transactions
    ADD CONSTRAINT payment_transactions_reference_no_key UNIQUE (reference_no);


--
-- Name: system_settings settig_key_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.system_settings
    ADD CONSTRAINT settig_key_pk PRIMARY KEY (setting_key);


--
-- Name: survey_tokens survey_tokens_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.survey_tokens
    ADD CONSTRAINT survey_tokens_pkey PRIMARY KEY (token_id);


--
-- Name: survey_tokens survey_tokens_token_string_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.survey_tokens
    ADD CONSTRAINT survey_tokens_token_string_key UNIQUE (token_string);


--
-- Name: idx_deliveries_payment_status; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_deliveries_payment_status ON public.deliveries USING btree (payment_status);


--
-- Name: idx_graduations_student_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_graduations_student_id ON public.graduations USING btree (student_id);


--
-- Name: attendance_logs attendance_logs_schedule_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.attendance_logs
    ADD CONSTRAINT attendance_logs_schedule_id_fkey FOREIGN KEY (schedule_id) REFERENCES public.mst_event_schedules(id) ON DELETE CASCADE;


--
-- Name: attendance_logs attendance_logs_student_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.attendance_logs
    ADD CONSTRAINT attendance_logs_student_id_fkey FOREIGN KEY (student_id) REFERENCES public.grad_students(id) ON DELETE CASCADE;


--
-- Name: deliveries fk_graduation; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.deliveries
    ADD CONSTRAINT fk_graduation FOREIGN KEY (graduation_id) REFERENCES public.graduations(id) ON DELETE CASCADE;


--
-- Name: graduations fk_student; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.graduations
    ADD CONSTRAINT fk_student FOREIGN KEY (student_id) REFERENCES public.grad_students(id) ON DELETE CASCADE;


--
-- Name: mst_shipping_rate mst_shipping_rate_shipping_method_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mst_shipping_rate
    ADD CONSTRAINT mst_shipping_rate_shipping_method_id_fkey FOREIGN KEY (shipping_method_id) REFERENCES public.mst_shipping_method(shipping_method_id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

\unrestrict IWze57H9TprkNaItOne3ETpMZ0wj9Ufj2U4FmR3EKuQf1sEwvkybjMtUsF2ymit

