CREATE DATABASE IF NOT EXISTS edabip_reports_db;

USE edabip_reports_db;

CREATE TABLE IF NOT EXISTS report_templates (
    id INT PRIMARY KEY AUTO_INCREMENT,
    template_name VARCHAR(150) NOT NULL,
    description VARCHAR(500),
    module VARCHAR(100) NOT NULL,
    created_by VARCHAR(100) NOT NULL,
    usage_count INT NOT NULL DEFAULT 0,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS reports (
    id INT PRIMARY KEY AUTO_INCREMENT,

    report_name VARCHAR(200) NOT NULL,

    module VARCHAR(100) NOT NULL,

    report_type ENUM(
        'Scheduled',
        'On Demand',
        'System Generated',
        'Ad-hoc'
    ) NOT NULL,

    last_run DATETIME NULL,

    owner VARCHAR(100) NOT NULL,

    status ENUM(
        'Completed',
        'Failed',
        'Scheduled'
    ) NOT NULL DEFAULT 'Scheduled',

    run_time_seconds INT NOT NULL DEFAULT 0,

    template_id INT NULL,

    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (template_id)
        REFERENCES report_templates(id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS report_activity (
    id INT PRIMARY KEY AUTO_INCREMENT,

    report_id INT NOT NULL,

    activity_type ENUM(
        'Generated',
        'Downloaded',
        'Re-run',
        'Failed'
    ) NOT NULL,

    activity_status ENUM(
        'Completed',
        'Failed',
        'Scheduled'
    ) NOT NULL,

    performed_by VARCHAR(100) NOT NULL,

    activity_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    details VARCHAR(500),

    FOREIGN KEY (report_id)
        REFERENCES reports(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE INDEX idx_reports_status
ON reports(status);

CREATE INDEX idx_reports_type
ON reports(report_type);

CREATE INDEX idx_reports_last_run
ON reports(last_run);

CREATE INDEX idx_reports_owner
ON reports(owner);

CREATE INDEX idx_activity_status
ON report_activity(activity_status);

CREATE INDEX idx_activity_time
ON report_activity(activity_time);

CREATE INDEX idx_activity_report
ON report_activity(report_id);