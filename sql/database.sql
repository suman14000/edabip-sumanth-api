CREATE DATABASE edabip_reports;
USE edabip_reports;
USE edabip_reports;

CREATE TABLE IF NOT EXISTS report_templates (
    id INT AUTO_INCREMENT PRIMARY KEY,
    template_name VARCHAR(150) NOT NULL UNIQUE,
    description TEXT,
    module VARCHAR(100) NOT NULL,
    created_by VARCHAR(100) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS reports (
    id INT AUTO_INCREMENT PRIMARY KEY,
    report_name VARCHAR(200) NOT NULL,
    module VARCHAR(100) NOT NULL,
    report_type ENUM('Scheduled', 'On Demand') NOT NULL,
    last_run DATETIME NULL,
    owner VARCHAR(100) NOT NULL,
    status ENUM('Completed', 'Failed', 'Scheduled')
        NOT NULL DEFAULT 'Scheduled',
    run_time_seconds DECIMAL(10,2) DEFAULT 0,
    template_id INT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_reports_template
        FOREIGN KEY (template_id)
        REFERENCES report_templates(id)
        ON DELETE SET NULL
        ON UPDATE CASCADE,
    INDEX idx_reports_module (module),
    INDEX idx_reports_type (report_type),
    INDEX idx_reports_status (status),
    INDEX idx_reports_owner (owner)
);
CREATE TABLE IF NOT EXISTS report_activity (
    id INT AUTO_INCREMENT PRIMARY KEY,
    report_id INT NOT NULL,
    activity_type VARCHAR(100) NOT NULL,
    activity_status ENUM('Success', 'Failed', 'Started')
        NOT NULL,
    message TEXT,
    execution_time_seconds DECIMAL(10,2) DEFAULT 0,
    executed_by VARCHAR(100),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_activity_report
        FOREIGN KEY (report_id)
        REFERENCES reports(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    INDEX idx_activity_report_id (report_id),
    INDEX idx_activity_status (activity_status)
);
SHOW TABLES;
INSERT INTO report_templates
(
    template_name,
    description,
    module,
    created_by
)
VALUES
(
    'Sales Template',
    'Standard sales reporting template',
    'Sales',
    'Admin'
),
(
    'Employee Template',
    'Employee and HR reporting template',
    'HR',
    'Admin'
),
(
    'Inventory Template',
    'Inventory and warehouse reporting template',
    'Inventory',
    'Admin'
),
(
    'Finance Template',
    'Financial reporting template',
    'Finance',
    'Admin'
),
(
    'Customer Template',
    'Customer analytics template',
    'Customer',
    'Admin'
);

SELECT * FROM report_templates;

INSERT INTO reports
(
    report_name,
    module,
    report_type,
    last_run,
    owner,
    status,
    run_time_seconds,
    template_id
)
VALUES
(
    'Monthly Sales Report',
    'Sales',
    'Scheduled',
    '2026-10-07 09:30:00',
    'Rahul',
    'Completed',
    12.50,
    1
),
(
    'Daily Sales Summary',
    'Sales',
    'Scheduled',
    '2026-10-08 08:00:00',
    'Priya',
    'Completed',
    8.20,
    1
),
(
    'Quarterly Revenue Report',
    'Finance',
    'Scheduled',
    '2026-10-01 10:00:00',
    'Arun',
    'Completed',
    18.40,
    4
),
(
    'Employee Attendance Report',
    'HR',
    'Scheduled',
    '2026-10-08 09:00:00',
    'Sumanth',
    'Completed',
    7.30,
    2
),
(
    'Payroll Summary Report',
    'HR',
    'Scheduled',
    '2026-10-01 09:15:00',
    'Kiran',
    'Completed',
    14.80,
    2
),
(
    'Inventory Status Report',
    'Inventory',
    'Scheduled',
    '2026-10-08 07:30:00',
    'Vijay',
    'Completed',
    10.60,
    3
),
(
    'Low Stock Report',
    'Inventory',
    'On Demand',
    '2026-10-07 14:20:00',
    'Anil',
    'Completed',
    5.40,
    3
),
(
    'Warehouse Performance Report',
    'Inventory',
    'Scheduled',
    '2026-10-06 16:00:00',
    'Meena',
    'Completed',
    16.20,
    3
),
(
    'Customer Activity Report',
    'Customer',
    'On Demand',
    '2026-10-07 11:45:00',
    'Priya',
    'Completed',
    9.70,
    5
),
(
    'Customer Retention Report',
    'Customer',
    'Scheduled',
    '2026-10-01 12:00:00',
    'Rahul',
    'Completed',
    21.30,
    5
),
(
    'Product Performance Report',
    'Sales',
    'On Demand',
    '2026-10-07 13:10:00',
    'Arun',
    'Completed',
    11.80,
    1
),
(
    'Regional Sales Report',
    'Sales',
    'Scheduled',
    '2026-10-06 09:00:00',
    'Kiran',
    'Completed',
    15.70,
    1
),
(
    'Department Performance Report',
    'HR',
    'On Demand',
    '2026-10-05 15:30:00',
    'Sumanth',
    'Completed',
    13.10,
    2
),
(
    'Leave Management Report',
    'HR',
    'Scheduled',
    '2026-10-08 08:30:00',
    'Meena',
    'Completed',
    6.90,
    2
),
(
    'Financial Summary Report',
    'Finance',
    'Scheduled',
    '2026-10-05 10:00:00',
    'Vijay',
    'Completed',
    19.40,
    4
),
(
    'Expense Analysis Report',
    'Finance',
    'On Demand',
    '2026-10-07 17:00:00',
    'Anil',
    'Completed',
    10.30,
    4
),
(
    'Profit Analysis Report',
    'Finance',
    'Scheduled',
    '2026-10-01 11:00:00',
    'Rahul',
    'Completed',
    23.50,
    4
),
(
    'Supplier Performance Report',
    'Inventory',
    'Scheduled',
    '2026-10-06 13:00:00',
    'Priya',
    'Completed',
    14.20,
    3
),
(
    'Purchase Order Report',
    'Inventory',
    'On Demand',
    '2026-10-07 12:15:00',
    'Arun',
    'Completed',
    8.90,
    3
),
(
    'Warehouse Inventory Report',
    'Inventory',
    'Scheduled',
    '2026-10-08 06:30:00',
    'Kiran',
    'Completed',
    17.60,
    3
),
(
    'Employee Performance Report',
    'HR',
    'On Demand',
    '2026-10-04 14:00:00',
    'Sumanth',
    'Failed',
    4.80,
    2
),
(
    'Recruitment Status Report',
    'HR',
    'Scheduled',
    '2026-10-08 07:00:00',
    'Meena',
    'Scheduled',
    0,
    2
),
(
    'Sales Forecast Report',
    'Sales',
    'Scheduled',
    NULL,
    'Rahul',
    'Scheduled',
    0,
    1
),
(
    'Customer Revenue Report',
    'Customer',
    'On Demand',
    '2026-10-03 16:45:00',
    'Priya',
    'Failed',
    3.70,
    5
),
(
    'Customer Segmentation Report',
    'Customer',
    'Scheduled',
    '2026-10-07 10:30:00',
    'Arun',
    'Completed',
    20.10,
    5
),
(
    'Order Analysis Report',
    'Sales',
    'On Demand',
    '2026-10-06 11:20:00',
    'Vijay',
    'Completed',
    9.50,
    1
),
(
    'Daily Operations Report',
    'Operations',
    'Scheduled',
    '2026-10-08 08:15:00',
    'Kiran',
    'Scheduled',
    0,
    NULL
),
(
    'System Health Report',
    'IT',
    'Scheduled',
    '2026-10-08 08:45:00',
    'Anil',
    'Completed',
    6.20,
    NULL
),
(
    'Data Quality Report',
    'Analytics',
    'On Demand',
    '2026-10-07 15:40:00',
    'Rahul',
    'Failed',
    5.10,
    NULL
),
(
    'Business KPI Report',
    'Analytics',
    'Scheduled',
    '2026-10-08 09:10:00',
    'Priya',
    'Completed',
    22.80,
    NULL
);

select * from reports;