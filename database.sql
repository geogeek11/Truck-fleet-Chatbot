CREATE TABLE truck (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    manufacturer VARCHAR(100),
    model VARCHAR(100),
    truck_number VARCHAR(100),
    color VARCHAR(100)
    );
    
INSERT INTO truck(manufacturer, model, truck_number, color) VALUES('SCANIA', 'S 730', '10', 'black');
INSERT INTO truck(manufacturer, model, truck_number, color) VALUES('SCANIA', 'S 730', '15', 'red');
INSERT INTO truck(manufacturer, model, truck_number, color) VALUES('SCANIA', 'S 730', '16', 'green');
INSERT INTO truck(manufacturer, model, truck_number, color) VALUES('SCANIA', 'G 410', '11', 'black');
INSERT INTO truck(manufacturer, model, truck_number, color) VALUES('VOLVO', 'FH16', '12', 'green');
INSERT INTO truck(manufacturer, model, truck_number, color) VALUES('VOLVO', 'LV40', '13', 'red');
INSERT INTO truck(manufacturer, model, truck_number, color) VALUES('VOLVO', 'FMX', '14', 'red');
INSERT INTO truck(manufacturer, model, truck_number, color) VALUES('VOLVO', 'FMX', '17', 'red');
INSERT INTO truck(manufacturer, model, truck_number, color) VALUES('VOLVO', 'FMX', '18', 'red');

CREATE TABLE log (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    message_text TEXT,
    is_bot INTEGER,
    created_at integer(4) not null default (strftime('%s','now'))
    );