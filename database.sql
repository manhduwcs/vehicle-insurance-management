CREATE DATABASE IF NOT EXISTS vehicleinsurancedb;
USE vehicleinsurancedb;

-- Independent tables first
CREATE TABLE Employees (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    Username VARCHAR(255) UNIQUE,
    Password VARCHAR(255),
    Fullname VARCHAR(255),
    Email VARCHAR(255) UNIQUE,
    Phone VARCHAR(50) UNIQUE,
    GroupID INT
);

CREATE TABLE Customers (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    Username VARCHAR(255) UNIQUE,
    Password VARCHAR(255),
    Fullname VARCHAR(255),
    Address TEXT,
    Email VARCHAR(255) UNIQUE,
    Phone VARCHAR(50) UNIQUE,
    IdentifyNumber VARCHAR(50),
    IdentifyAddress VARCHAR(255),
    IdentifyDate DATE,
    IssuingAuthority VARCHAR(255),
    TaxID VARCHAR(50)
);

CREATE TABLE VehicleTypes (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(255),
    Fee DECIMAL(10,2),
    Description TEXT,
    MaxPersonalCompensation DECIMAL(15,2),
    MaxPropertyCompensation DECIMAL(15,2)
);

CREATE TABLE InsuranceCategories (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(255),
    Description TEXT
);

CREATE TABLE Duration (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    Months DECIMAL(5,2)
);

CREATE TABLE Functions (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    FunctionName VARCHAR(255),
    Description TEXT
);

CREATE TABLE Actions (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    ActionName VARCHAR(255),
    Description TEXT
);

CREATE TABLE GroupsUsers (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    GroupName VARCHAR(255),
    Description TEXT
);

-- Dependent tables
CREATE TABLE Vehicles (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(255),
    CustomerID INT,
    Model VARCHAR(255),
    VehicleTypeID INT,
    PurchasePrice DECIMAL(15,2),
    BodyNumber VARCHAR(50),
    EngineNumber VARCHAR(50),
    Number VARCHAR(50),
    RegistrationDate DATE,
    FOREIGN KEY (CustomerID) REFERENCES Customers(ID),
    FOREIGN KEY (VehicleTypeID) REFERENCES VehicleTypes(ID)
);

CREATE TABLE InsurancePriceList (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    InsuranceCategoryID INT,
    DurationID INT,
    MinAge INT,
    MaxAge INT,
    Rate DECIMAL(5,2),
    FOREIGN KEY (InsuranceCategoryID) REFERENCES InsuranceCategories(ID),
    FOREIGN KEY (DurationID) REFERENCES Duration(ID)
);

CREATE TABLE Contracts (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    ContractNo VARCHAR(255) UNIQUE,
    VehicleID INT,
    InsuranceCategoryID INT,
    EstimateValue DECIMAL(15,2),
    EstimatePremium DECIMAL(15,2),
    DeductibleValue DECIMAL(15,2),
    DeductibleAddon DECIMAL(15,2),
    DurationID INT,
    ActualValue DECIMAL(15,2),
    ActualPremium DECIMAL(15,2),
    FixedDeduction DECIMAL(15,2),
    MaxPersonCompensation DECIMAL(15,2),
    AvailablePersonCompensation DECIMAL(15,2),
    AvailablePropertyCompensation DECIMAL(15,2),
    StartDate DATE,
    Status ENUM('Awaiting','Pending','Rejected','Actived','Canceled','Inactived'),
    Note TEXT,
    CreatedBy INT,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (VehicleID) REFERENCES Vehicles(ID),
    FOREIGN KEY (InsuranceCategoryID) REFERENCES InsuranceCategories(ID),
    FOREIGN KEY (DurationID) REFERENCES Duration(ID),
    FOREIGN KEY (CreatedBy) REFERENCES Employees(ID)
);

CREATE TABLE Claims (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    ClaimNo VARCHAR(255) UNIQUE,
    CustomerID INT,
    VehicleID INT,
    ContractID INT,
    Place TEXT,
    Date DATE,
    HumanDamage DECIMAL(15,2),
    PropertyDamage DECIMAL(15,2),
    Deduction DECIMAL(15,2),
    PersonalCompensation DECIMAL(15,2),
    PropertyCompensation DECIMAL(15,2),
    Note TEXT,
    Status ENUM('Pending','Approved','Completed','Rejected'),
    FOREIGN KEY (CustomerID) REFERENCES Customers(ID),
    FOREIGN KEY (VehicleID) REFERENCES Vehicles(ID),
    FOREIGN KEY (ContractID) REFERENCES Contracts(ID)
);

CREATE TABLE Expenses (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    Content TEXT,
    Amount DECIMAL(15,2),
    Date DATE
);

CREATE TABLE GroupsFunctionsActions (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    GroupID INT,
    FunctionID INT,
    ActionID INT,
    FOREIGN KEY (GroupID) REFERENCES GroupsUsers(ID),
    FOREIGN KEY (FunctionID) REFERENCES Functions(ID),
    FOREIGN KEY (ActionID) REFERENCES Actions(ID)
);

-- sample data 
USE vehicleinsurancedb;

-- Customers
INSERT INTO Customers (Username, Password, Fullname, Address, Email, Phone, IdentifyNumber, IdentifyAddress, IdentifyDate, IssuingAuthority, TaxID)
VALUES
('johnsmith', '123456', 'John Smith', '12 Nguyen Trai, District 1, Ho Chi Minh City', 'john.smith@example.com', '0903123456', '123456789', 'Ho Chi Minh City', '2020-05-12', 'Police Dept HCM', 'TX00123'),
('emilytran', '123456', 'Emily Tran', '45 Cau Giay, Hanoi', 'emily.tran@example.com', '0987234567', '987654321', 'Hanoi', '2021-03-20', 'Police Dept Hanoi', 'TX00456'),
('michaelle', '123456', 'Michael Le', '89 Le Loi, Da Nang', 'michael.le@example.com', '0934567890', '223344556', 'Da Nang', '2021-08-09', 'Police Dept Da Nang', 'TX00789'),
('hannahpham', '123456', 'Hannah Pham', '21 Nguyen Hue, Hue City', 'hannah.pham@example.com', '0976543210', '112233445', 'Hue', '2022-01-12', 'Police Dept Hue', 'TX01001'),
('ethannam', '123456', 'Ethan Nam', '5 Ly Thuong Kiet, Hai Phong', 'ethan.nam@example.com', '0912789345', '334455667', 'Hai Phong', '2020-09-30', 'Police Dept Hai Phong', 'TX01234');

-- VehicleTypes
INSERT INTO VehicleTypes (Name, Fee, Description, MaxPersonalCompensation, MaxPropertyCompensation)
VALUES
-- Motorcycles
('Motorcycle under 50cc', 55000, 'Motorcycle with engine capacity under 50cc', 150000000, 100000000),
('Motorcycle over 50cc', 60000, 'Motorcycle with engine capacity over 50cc', 150000000, 100000000),

-- Passenger cars
('Car under 6 seats (non-commercial)', 437000, 'Private passenger car under 6 seats (non-commercial use)', 150000000, 100000000),
('Car from 6 to 11 seats', 794000, 'Passenger car with 6–11 seats', 150000000, 100000000),
('Commercial car under 6 seats', 756000, 'Commercial passenger car under 6 seats', 150000000, 100000000),

-- Trucks and trailers
('Truck under 3.5 tons', 853000, 'Truck with payload under 3.5 tons', 150000000, 100000000),
('Truck from 3.5 to 7 tons', 1660000, 'Truck with payload from 3.5 to 7 tons', 150000000, 100000000),
('Tractor head', 1826000, 'Semi-trailer tractor head', 150000000, 100000000);

-- Vehicles
INSERT INTO Vehicles (Name, CustomerID, Model, VehicleTypeID, PurchasePrice, BodyNumber, EngineNumber, Number, RegistrationDate)
VALUES
-- Customer 1
('Toyota Vios', 1, 'Vios G 2021', 3, 560000000, 'TH12345', 'EN98765', '30A-45678', '2022-05-12'),
('Yamaha Janus', 1, 'Janus 125cc 2022', 2, 41000000, 'THA001', 'ENA001', '29H1-22345', '2023-03-15'),

-- Customer 2
('Honda City', 2, 'City RS 2022', 3, 620000000, 'TH54321', 'EN12345', '30B-56789', '2023-02-10'),
('Hyundai Staria', 2, 'Staria 9-Seater 2023', 4, 1380000000, 'THB002', 'ENB002', '30D-77788', '2023-11-02'),

-- Customer 3
('Yamaha Exciter', 3, 'Exciter 155', 2, 48000000, 'TH88888', 'EN77777', '29E1-12345', '2023-06-20'),
('Ford Transit', 3, 'Transit 2020', 4, 1120000000, 'THC003', 'ENC003', '30E-99234', '2020-09-09'),

-- Customer 4
('Kia K200', 4, 'K200 1.9 Ton', 6, 465000000, 'TH99999', 'EN66666', '29C-88888', '2021-11-05'),
('Isuzu NQR75', 4, 'NQR75 5-Ton Truck', 7, 780000000, 'THD004', 'END004', '30C-55555', '2022-08-20'),
('Hino 700', 4, 'Hino 700 Tractor Head', 8, 1650000000, 'THE004', 'ENE004', '30H-11111', '2023-01-15'),

-- Customer 5
('Mazda CX-5', 5, 'CX-5 Premium 2023', 3, 850000000, 'TH11223', 'EN33445', '30F-99999', '2023-09-01'),
('Suzuki Carry', 5, 'Carry Truck 2022', 6, 365000000, 'THF005', 'ENF005', '30G-66666', '2022-06-30');


-- InsuranceCategories 
INSERT INTO InsuranceCategories (Name, Description)
VALUES
('Comprehensive car insurance', 'Comprehensive car insurance covers damage from accidents, theft, fire, vandalism, or natural disasters'),
('Hydrolock insurance', 'Hydrolock insurance covers damage caused when water enters the engine (hydrolock) during flooding'),
('Theft insurance', 'Theft insurance covers loss or damage caused by theft or attempted theft'),
('Fire and explosion insurance', 'Fire and explosion insurance covers loss or damage caused by fire, explosion, or related incidents'),
('Natural disaster insurance', 'Natural disaster insurance covers loss or damage caused by natural disasters such as floods, storms, earthquakes, or typhoons');

-- Duration
INSERT INTO Duration (Months)
VALUES
(12),
(24),
(36);

-- InsurancePriceList demo data
INSERT INTO InsurancePriceList (InsuranceCategoryID, DurationID, MinAge, MaxAge, Rate) VALUES
-- 1. Body Damage Insurance (Thân vỏ)
(1, 1, 0, 3, 1.30),
(1, 1, 4, 7, 1.50),
(1, 1, 8, 10, 1.80),
(1, 1, 11, 20, 2.00),
(1, 2, 0, 3, 1.25),
(1, 2, 4, 7, 1.45),
(1, 2, 8, 10, 1.70),
(1, 2, 11, 20, 1.90),
(1, 3, 0, 3, 1.20),
(1, 3, 4, 7, 1.40),
(1, 3, 8, 10, 1.60),
(1, 3, 11, 20, 1.80),

-- 2. Flood Damage (Thủy kích)
(2, 1, 0, 3, 0.20),
(2, 1, 4, 7, 0.25),
(2, 1, 8, 10, 0.30),
(2, 1, 11, 20, 0.35),
(2, 2, 0, 3, 0.19),
(2, 2, 4, 7, 0.23),
(2, 2, 8, 10, 0.28),
(2, 2, 11, 20, 0.33),
(2, 3, 0, 3, 0.18),
(2, 3, 4, 7, 0.22),
(2, 3, 8, 10, 0.27),
(2, 3, 11, 20, 0.32),

-- 3. Theft Insurance (Mất cắp)
(3, 1, 0, 3, 0.40),
(3, 1, 4, 7, 0.45),
(3, 1, 8, 10, 0.50),
(3, 1, 11, 20, 0.60),
(3, 2, 0, 3, 0.38),
(3, 2, 4, 7, 0.43),
(3, 2, 8, 10, 0.48),
(3, 2, 11, 20, 0.57),
(3, 3, 0, 3, 0.36),
(3, 3, 4, 7, 0.41),
(3, 3, 8, 10, 0.46),
(3, 3, 11, 20, 0.55),

-- 4. Fire & Explosion (Cháy nổ)
(4, 1, 0, 3, 0.15),
(4, 1, 4, 7, 0.18),
(4, 1, 8, 10, 0.20),
(4, 1, 11, 20, 0.25),
(4, 2, 0, 3, 0.14),
(4, 2, 4, 7, 0.17),
(4, 2, 8, 10, 0.19),
(4, 2, 11, 20, 0.23),
(4, 3, 0, 3, 0.13),
(4, 3, 4, 7, 0.16),
(4, 3, 8, 10, 0.18),
(4, 3, 11, 20, 0.22),

-- 5. Natural Disaster (Thiên tai)
(5, 1, 0, 3, 0.25),
(5, 1, 4, 7, 0.30),
(5, 1, 8, 10, 0.35),
(5, 1, 11, 20, 0.40),
(5, 2, 0, 3, 0.24),
(5, 2, 4, 7, 0.28),
(5, 2, 8, 10, 0.33),
(5, 2, 11, 20, 0.38),
(5, 3, 0, 3, 0.23),
(5, 3, 4, 7, 0.27),
(5, 3, 8, 10, 0.32),
(5, 3, 11, 20, 0.37);

-- Expenses
INSERT INTO Expenses (Content, Amount, Date)
VALUES
('Office rent', 5000000, '2025-01-01'),
('Electricity bill', 1200000, '2025-01-15'),
('Internet bill', 800000, '2025-01-20'),
('Computer system maintenance', 2500000, '2025-02-05'),
('Online advertising cost', 3500000, '2025-02-10'),
('Office supplies purchase', 950000, '2025-02-18'),
('Water bill', 600000, '2025-03-01'),
('Building cleaning service', 1000000, '2025-03-10'),
('Company vehicle maintenance', 4200000, '2025-03-25');

INSERT INTO GroupsUsers (GroupName, Description)
VALUES 
    ('Administrator', 'Manage employees, customers, groups users'),
    ('Customer', 'Customers'),
    ('Employee', 'Employees');

INSERT INTO Employees(Username, Fullname, Email, Phone, Password, GroupID)
VALUES 
    ('admin', 'Administrator', 'admin@gmail.com', '0999999999', '123456', 1),
    ('customer1', 'Nguyen Van A', 'nva@gmail.com', '0888888888', '123456', 2),
    ('employee1', 'Hoang Anh B', 'hab@gmail.com', '0777777777', '123456', 3);

INSERT INTO Functions (FunctionName, Description) VALUES
    ('Manage Customers', 'Manage Customers'),
    ('Manage Vehicles', 'Manage Vehicles'),
    ('Manage Vehicle Types', 'Manage Vehicle Types'),
    ('Manage Contracts', 'Manage Contracts'),
    ('Manage Claims', 'Manage Claims'),
    ('Manage Expenses', 'Manage Expenses'),
    ('Manage Employees', 'Manage Employees'),
    ('Manage Groups users', 'Manage Groups Users'),
    ('Manage Insurance Categories', 'Manage Insurance Categories'),
    ('Manage Insurance Price List', 'Manage Insurance Price List');

INSERT INTO Actions (ActionName, Description)
VALUES 
    ('View', 'View Info'),
    ('Create', 'Add new data'),
    ('Edit', 'Update data'),
    ('Delete', 'Delete data'),
    ('Download', 'Download data'),
    ('Print', 'Print data'),
    ('Export', 'Export data');

INSERT INTO GroupsFunctionsActions (GroupID, FunctionID, ActionID)
VALUES 
    -- Administrator
    (1, 1, 1), (1, 1, 2), (1, 1, 3), (1, 1, 4),
    (1, 7, 1), (1, 7, 2), (1, 7, 3), (1, 7, 4),
    (1, 8, 1), (1, 8, 2), (1, 8, 3), (1, 8, 4),

    -- Customers
    (2, 1, 1), (2, 1, 2), (2, 1, 3), 
    (2, 2, 1), (2, 2, 2), (2, 2, 3), (2, 2, 4), 
    (2, 4, 1), (2, 4, 2), (2, 4, 3), (2, 4, 5), (2, 4, 6), 
    (2, 5, 1), (2, 5, 2), (2, 5, 3), (2, 5, 5), (2, 5, 6), 
    
    -- Employees
    (3, 3, 1), (3, 3, 2), (3, 3, 3), (3, 3, 4), 
    (3, 4, 1), (3, 4, 2), (3, 4, 3), (3, 4, 4), (3, 4, 5), (3, 4, 6), 
    (3, 5, 1), (3, 5, 2), (3, 5, 3), (3, 5, 4), (3, 5, 5), (3, 5, 6), 
    (3, 6, 1), (3, 6, 2), (3, 6, 3), (3, 6, 4), 
    (3, 9, 1), (3, 9, 2), (3, 9, 3), (3, 9, 4), 
    (3, 10, 1), (3, 10, 2), (3, 10, 3), (3, 10, 4);
