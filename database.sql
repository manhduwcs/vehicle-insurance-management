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
    TaxID VARCHAR(50),
    GroupID INT
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
    Description TEXT,
    Images TEXT
);

CREATE TABLE Duration (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    Months INT
);


CREATE TABLE Depreciations (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    Age INT,
    Rate DECIMAL(5,2)
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
    RatePremium DECIMAL(5,2),
    MaxCoverageRate DECIMAL(5,2),
    FOREIGN KEY (InsuranceCategoryID) REFERENCES InsuranceCategories(ID),
    FOREIGN KEY (DurationID) REFERENCES Duration(ID)
);

CREATE TABLE Contracts ( ID INT PRIMARY KEY AUTO_INCREMENT,
    ContractNo VARCHAR(255) UNIQUE,
    CreatedBy INT,
    VehicleID INT,
    InsuranceCategoryID INT,
    EstimateValue DECIMAL(15,2),
    EstimatePremium DECIMAL(15,2),
    DurationID INT,
    DeductibleValue DECIMAL(15,2),
    DeductibleAddon DECIMAL(15,2),
    ActualValue DECIMAL(15,2),
    ActualPremium DECIMAL(15,2),
    FixedDeduction DECIMAL(15,2),
    MaxPersonCompensation DECIMAL(15,2),
    MaxPropertyCompensation DECIMAL(15,2),
    AvailablePersonCompensation DECIMAL(15,2),
    AvailablePropertyCompensation DECIMAL(15,2),
    StartDate DATE,
    Status ENUM('Awaiting','Pending','Rejected','Actived','Canceled','Inactived'),
    Note TEXT,
    PaymentType VARCHAR(20),          
    PaymentAt DATETIME,               
    PaymentAmount DECIMAL(15,2),      -- ✅ added
    UpdatedBy INT,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (VehicleID) REFERENCES Vehicles(ID),
    FOREIGN KEY (InsuranceCategoryID) REFERENCES InsuranceCategories(ID),
    FOREIGN KEY (DurationID) REFERENCES Duration(ID),
    FOREIGN KEY (CreatedBy) REFERENCES Customers(ID),
    FOREIGN KEY (UpdatedBy) REFERENCES Employees(ID)
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

-- Keys
ALTER TABLE Customers
ADD CONSTRAINT fk_customer_group
FOREIGN KEY (GroupID)
REFERENCES GroupsUsers(ID)
ON DELETE SET NULL;


-- sample data 
USE vehicleinsurancedb;

-- VehicleTypes
INSERT INTO VehicleTypes (Name, Fee, Description, MaxPersonalCompensation, MaxPropertyCompensation)
VALUES
-- I. Motorbikes (2-wheel)
('Motorcycle - under 50 cc', 55000, 'Two-wheeled motorcycle, engine capacity under 50 cc', 150000000, 50000000),
('Motorcycle - 50 cc or more', 60000, 'Two-wheeled motorcycle, engine capacity 50 cc or more', 150000000, 50000000),

-- II. Three-wheeled motorcycle
('Three-wheeled motorcycle', 290000, 'Three-wheeled motorcycle', 150000000, 50000000),

-- III. Powered bicycles / e-bikes and other similar
('Electric motorcycle / e-bike', 55000, 'Electric motorcycle / e-bike', 150000000, 50000000),
('Other similar motorized small vehicles', 290000, 'Other motorized similar vehicles', 150000000, 50000000),

-- IV. Private (non-commercial) cars (by seats)
('Private car (under 6 seats)', 437000, 'Private passenger car, under 6 seats', 150000000, 100000000),
('Private car (6 to 11 seats)', 794000, 'Private passenger car, 6–11 seats', 150000000, 100000000),
('Private car (12 to 24 seats)', 1270000, 'Private passenger car, 12–24 seats', 150000000, 100000000),
('Private car (over 24 seats)', 1825000, 'Private passenger car, over 24 seats', 150000000, 100000000),
('Private Pickup / Minivan', 437000, 'Pickup or minivan used for private purposes', 150000000, 100000000),

-- V. Commercial passenger vehicles (by seats, grouped)
('Commercial passenger vehicle (under 6 seats)', 756000, 'Commercial passenger vehicle, under 6 seats', 150000000, 100000000),
('Commercial passenger vehicle (6–11 seats)', 1080000, 'Commercial passenger vehicle, 6–11 seats', 150000000, 100000000),
('Commercial passenger vehicle (12–24 seats)', 2049000, 'Commercial passenger vehicle, 12–24 seats', 150000000, 100000000),
('Commercial passenger vehicle (over 24 seats)', 4813000, 'Commercial passenger vehicle, over 24 seats', 150000000, 100000000),
('Commercial Pickup / Minivan', 933000, 'Pickup or minivan used for commercial purposes', 150000000, 100000000),
('Taxi', 1285200, 'Taxi (170% of commercial vehicle under 6 seats)', 150000000, 100000000),
('Driver training vehicle', 908400, 'Driver training vehicle (120% of private car under 6 seats)', 150000000, 100000000),
('Ambulance', 1119600, 'Ambulance or emergency vehicle (120% of commercial pickup fee)', 150000000, 100000000),
('Cash transport / Security vehicle', 907200, 'Special-purpose security or cash transport vehicle (120% of private car under 6 seats)', 150000000, 100000000),
('Tractor–Semi-trailer', 4800000, 'Tractor and semi-trailer (150% of truck over 15 tons)', 150000000, 100000000),
('Agricultural tractor', 1023600, 'Agricultural tractor and trailer (120% of truck under 3 tons)', 150000000, 100000000);


-- InsuranceCategories 
INSERT INTO InsuranceCategories (Name, Description)
VALUES
('Civil liability insurance', 'Civil liability insurance is insurance that covers the policyholder’s legal responsibility for damage or injury caused to other people or their property'),
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

-- Depreciations
INSERT INTO Depreciations (Age, Rate)
VALUES
(0, 1.00),
(1, 0.90),
(2, 0.85),
(3, 0.80),
(4, 0.73),
(5, 0.67),
(6, 0.61),
(7, 0.55),
(8, 0.50),
(9, 0.45),
(10, 0.40),
(11, 0.35),
(12, 0.31),
(13, 0.27),
(14, 0.24),
(15, 0.21),
(16, 0.18),
(17, 0.15),
(18, 0.12),
(19, 0.10),
(20, 0.08);

-- InsurancePriceList demo data
INSERT INTO InsurancePriceList (InsuranceCategoryID, DurationID, MinAge, MaxAge, RatePremium, MaxCoverageRate) VALUES
-- 1. Civil liability insurance
(1, 1, 0, 3, 100, 100),
(1, 1, 4, 7, 100, 100),
(1, 1, 8, 10, 100, 100),
(1, 1, 11, 20, 100, 100),
(1, 2, 0, 3, 95, 100),
(1, 2, 4, 7, 95, 100),
(1, 2, 8, 10, 95, 100),
(1, 2, 11, 20, 95, 100),
(1, 3, 0, 3, 90, 100),
(1, 3, 4, 7, 90, 100),
(1, 3, 8, 10, 90, 100),
(1, 3, 11, 20, 90, 100),

-- 2. Body Damage Insurance
(2, 1, 0, 3, 1.30, 100),
(2, 1, 4, 7, 1.50, 100),
(2, 1, 8, 10, 1.80, 100),
(2, 1, 11, 20, 2.00, 100),
(2, 2, 0, 3, 1.25, 100),
(2, 2, 4, 7, 1.45, 100),
(2, 2, 8, 10, 1.70, 100),
(2, 2, 11, 20, 1.90, 100),
(2, 3, 0, 3, 1.20, 100),
(2, 3, 4, 7, 1.40, 100),
(2, 3, 8, 10, 1.60, 100),
(2, 3, 11, 20, 1.80, 100),

-- 3. Hydrolock Damage
(3, 1, 0, 3, 0.20, 35),
(3, 1, 4, 7, 0.25, 35),
(3, 1, 8, 10, 0.30, 35),
(3, 1, 11, 20, 0.35, 35),
(3, 2, 0, 3, 0.19, 35),
(3, 2, 4, 7, 0.23, 35),
(3, 2, 8, 10, 0.28, 35),
(3, 2, 11, 20, 0.33, 35),
(3, 3, 0, 3, 0.18, 35),
(3, 3, 4, 7, 0.22, 35),
(3, 3, 8, 10, 0.27, 35),
(3, 3, 11, 20, 0.32, 35),

-- 4. Theft Insurance
(4, 1, 0, 3, 0.40, 100),
(4, 1, 4, 7, 0.45, 100),
(4, 1, 8, 10, 0.50, 100),
(4, 1, 11, 20, 0.60, 100),
(4, 2, 0, 3, 0.38, 100),
(4, 2, 4, 7, 0.43, 100),
(4, 2, 8, 10, 0.48, 100),
(4, 2, 11, 20, 0.57, 100),
(4, 3, 0, 3, 0.36, 100),
(4, 3, 4, 7, 0.41, 100),
(4, 3, 8, 10, 0.46, 100),
(4, 3, 11, 20, 0.55, 100),

-- 5. Fire & Explosion
(5, 1, 0, 3, 0.15, 80),
(5, 1, 4, 7, 0.18, 80),
(5, 1, 8, 10, 0.20, 80),
(5, 1, 11, 20, 0.25, 80),
(5, 2, 0, 3, 0.14, 80),
(5, 2, 4, 7, 0.17, 80),
(5, 2, 8, 10, 0.19, 80),
(5, 2, 11, 20, 0.23, 80),
(5, 3, 0, 3, 0.13, 80),
(5, 3, 4, 7, 0.16, 80),
(5, 3, 8, 10, 0.18, 80),
(5, 3, 11, 20, 0.22, 80),

-- 6. Natural Disaster
(6, 1, 0, 3, 0.25, 90),
(6, 1, 4, 7, 0.30, 90),
(6, 1, 8, 10, 0.35, 90),
(6, 1, 11, 20, 0.40, 90),
(6, 2, 0, 3, 0.24, 90),
(6, 2, 4, 7, 0.28, 90),
(6, 2, 8, 10, 0.33, 90),
(6, 2, 11, 20, 0.38, 90),
(6, 3, 0, 3, 0.23, 90),
(6, 3, 4, 7, 0.27, 90),
(6, 3, 8, 10, 0.32, 90),
(6, 3, 11, 20, 0.37, 90);

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

INSERT INTO Functions (FunctionName, Description) VALUES
    ('Manage Customers by Customers', 'Manage Customers by Customers'),
    ('Manage Customers by Employees', 'Manage Customers by Employees'),
    ('Manage Vehicles', 'Manage Vehicles'),
    ('Manage Vehicle Types', 'Manage Vehicle Types'),
    ('Manage Contracts by Customers', 'Manage Contracts by Customers'),
    ('Manage Contracts by Employees', 'Manage Contracts by Employees'),
    ('Manage Claims by Customers', 'Manage Claims by Customers'),
    ('Manage Claims by Employees', 'Manage Claims by Employees'),
    ('Manage Expenses', 'Manage Expenses'),
    ('Manage Employees by Admin', 'Manage Employees by Admin'),
    ('Manage Employees by Employees', 'Manage Employees by Employees'),
    ('Manage Groups users', 'Manage Groups Users'),
    ('Manage Insurance Categories', 'Manage Insurance Categories'),
    ('Manage Insurance Price List', 'Manage Insurance Price List'),
    ('Manage Home', 'Manage Home Page');

INSERT INTO Actions (ActionName, Description)
VALUES 
    ('View', 'View Info'),
    ('Create', 'Add new data'),
    ('Edit', 'Update data'),
    ('Delete', 'Delete data');

INSERT INTO GroupsFunctionsActions (GroupID, FunctionID, ActionID)
VALUES 
    -- Administrator
    (1, 10, 1), (1, 10, 2), (1, 10, 3), (1, 10, 4),
    (1, 12, 1), (1, 12, 2), (1, 12, 3), (1, 12, 4),
    (1, 15, 1), 

    -- Customers
    (2, 1, 1), (2, 1, 2), (2, 1, 3), 
    (2, 3, 1), (2, 3, 2), (2, 3, 3), (2, 3, 4), 
    (2, 5, 1), (2, 5, 2), (2, 5, 3), 
    (2, 7, 1), (2, 7, 2), (2, 7, 3), 
    
    -- Employees
    (3, 2, 1),
    (3, 3, 1),
    (3, 4, 1), (3, 4, 2), (3, 4, 3), (3, 4, 4),
    (3, 6, 1), (3, 3, 3), 
    (3, 8, 1), (3, 3, 3),
    (3, 9, 1), (3, 9, 2), (3, 9, 3), (3, 9, 4),
    (3, 11, 1), (3, 11, 3), 
    (3, 13, 1), (3, 13, 2), (3, 13, 3), (3, 13, 4),
    (3, 14, 1), (3, 14, 3),
    (3, 15, 1);

-- Employees
INSERT INTO Employees(Username, Fullname, Email, Phone, Password, GroupID)
VALUES 
    ('admin', 'Administrator', 'admin@gmail.com', '0999999999', '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', 1),
    ('employee1', 'Hoang Anh B', 'hab@gmail.com', '0777777777', '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', 3);

-- Customers
INSERT INTO Customers (Username, Password, Fullname, Address, Email, Phone, IdentifyNumber, IdentifyAddress, IdentifyDate, IssuingAuthority, TaxID, GroupID)
VALUES
('johnsmith', 'pbkdf2_sha256$1000000$gLf5msigu4GH8dBxh3T23Y$x6k36F9OUhaCx9ZXH3sbx5Yc0ZgsqeHhTtgOr6PCTrE=', 'John Smith', '12 Nguyen Trai, District 1, Ho Chi Minh City', 'john.smith@example.com', '0903123456', '123456789', 'Ho Chi Minh City', '2020-05-12', 'Police Dept HCM', 'TX00123', 2),
('emilytran', 'pbkdf2_sha256$1000000$gLf5msigu4GH8dBxh3T23Y$x6k36F9OUhaCx9ZXH3sbx5Yc0ZgsqeHhTtgOr6PCTrE=', 'Emily Tran', '45 Cau Giay, Hanoi', 'emily.tran@example.com', '0987234567', '987654321', 'Hanoi', '2021-03-20', 'Police Dept Hanoi', 'TX00456', 2),
('michaelle', 'pbkdf2_sha256$1000000$gLf5msigu4GH8dBxh3T23Y$x6k36F9OUhaCx9ZXH3sbx5Yc0ZgsqeHhTtgOr6PCTrE=', 'Michael Le', '89 Le Loi, Da Nang', 'michael.le@example.com', '0934567890', '223344556', 'Da Nang', '2021-08-09', 'Police Dept Da Nang', 'TX00789', 2),
('hannahpham', 'pbkdf2_sha256$1000000$gLf5msigu4GH8dBxh3T23Y$x6k36F9OUhaCx9ZXH3sbx5Yc0ZgsqeHhTtgOr6PCTrE=', 'Hannah Pham', '21 Nguyen Hue, Hue City', 'hannah.pham@example.com', '0976543210', '112233445', 'Hue', '2022-01-12', 'Police Dept Hue', 'TX01001', 2),
('ethannam', 'pbkdf2_sha256$1000000$gLf5msigu4GH8dBxh3T23Y$x6k36F9OUhaCx9ZXH3sbx5Yc0ZgsqeHhTtgOr6PCTrE=', 'Ethan Nam', '5 Ly Thuong Kiet, Hai Phong', 'ethan.nam@example.com', '0912789345', '334455667', 'Hai Phong', '2020-09-30', 'Police Dept Hai Phong', 'TX01234', 2);


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

