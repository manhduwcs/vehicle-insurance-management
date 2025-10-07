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
    MaxClaimableAmount DECIMAL(15,2)
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
    Years INT,
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
    DeductibleRate DECIMAL(5,2),
    DeductibleAddon DECIMAL(15,2),
    ActualValue DECIMAL(15,2),
    ActualPremium DECIMAL(15,2),
    FixedDeduction DECIMAL(15,2),
    AvaiableClaimAmount DECIMAL(15,2),
    StartDate DATE,
    Status ENUM('Awaiting','Reject','Pending','Active','Inactive'),
    Note TEXT,
    CreatedBy INT,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (VehicleID) REFERENCES Vehicles(ID),
    FOREIGN KEY (InsuranceCategoryID) REFERENCES InsuranceCategories(ID),
    FOREIGN KEY (CreatedBy) REFERENCES Employees(ID)
);

CREATE TABLE Claims (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    ClaimNo VARCHAR(255) UNIQUE,
    CustomerID INT,
    VehicleID INT,
    ContractID INT,
    InsuranceCategoryID INT,  
    Place TEXT,
    Date DATE,
    DamageAmount DECIMAL(15,2),
    Deduction DECIMAL(15,2),
    ClaimAmount DECIMAL(15,2),
    Status ENUM('Pending','Approved','Completed','Rejected'),
    FOREIGN KEY (CustomerID) REFERENCES Customers(ID),
    FOREIGN KEY (VehicleID) REFERENCES Vehicles(ID),
    FOREIGN KEY (ContractID) REFERENCES Contracts(ID),
    FOREIGN KEY (InsuranceCategoryID) REFERENCES InsuranceCategories(ID)
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
INSERT INTO Customers (Username, Password, Fullname, Address, Email, Phone, IdentifyNumber, IdentifyAddress, IdentifyDate, IssuingAuthority, TaxID) VALUES
('nguyen.van.a', '123456!', 'Nguyen Van A', '123 Le Loi, Hanoi', 'nvana@gmail.com', '0912345678', 'C123456789', 'Hanoi', '2015-01-01', 'Hanoi Police', 'TAX12345'),
('tran.thi.b', '123456!', 'Tran Thi B', '456 Tran Hung Dao, HCMC', 'ttb@gmail.com', '0912345679', 'C987654321', 'HCMC', '2016-05-15', 'HCMC Police', 'TAX54321'),
('le.van.c', '123456!', 'Le Van C', '789 Nguyen Trai, Danang', 'lvc@gmail.com', '0912345680', 'C192837465', 'Danang', '2017-09-10', 'Danang Police', 'TAX67890');

-- VehicleTypes
INSERT INTO VehicleTypes (Name, Fee, Description, MaxClaimableAmount) VALUES
('Sedan', 500, '4-door car', 200000000),
('SUV', 800, 'Sports Utility Vehicle', 300000000),
('Truck', 1000, 'Cargo truck', 400000000),
('Motorbike', 100, 'Two-wheeled motorbike', 50000000);

-- Vehicles
INSERT INTO Vehicles (Name, CustomerID, Model, VehicleTypeID, PurchasePrice, BodyNumber, EngineNumber, Number, RegistrationDate) VALUES
('Toyota Camry', 1, 'Camry 2020', 1, 1000000000, 'B12345', 'E54321', '30A-12345', '2020-01-15'),
('Honda CRV', 2, 'CRV 2019', 2, 1200000000, 'B67890', 'E09876', '30B-67890', '2019-03-20'),
('Ford Ranger', 3, 'Ranger 2021', 3, 1500000000, 'B11122', 'E22211', '43C-11223', '2021-07-10'),
('Yamaha Exciter', 1, 'Exciter 150', 4, 50000000, 'B33344', 'E44433', '29A-33445', '2018-05-05');

-- InsuranceCategories
INSERT INTO InsuranceCategories (Name, Description) VALUES
('Third Party Liability', 'Insurance covers damage to third party'),
('Comprehensive', 'Covers own damage + third party'),
('Motorbike Liability', 'Covers motorbike accidents');

-- Duration
INSERT INTO Duration (Months) VALUES (6), (12), (24);

-- InsurancePriceList (based on your image)
INSERT INTO InsurancePriceList (InsuranceCategoryID, DurationID, Years, Rate) VALUES
(1, 2, 1, 1.5),
(2, 2, 1, 2.0),
(2, 3, 2, 3.8),
(3, 1, 0.5, 0.8);


-- Expenses
INSERT INTO Expenses (Content, Amount, Date)
VALUES
('Office rent', 5000000, '2025-01-01'),
('Electricity', 1200000, '2025-01-15'),
('Internet', 800000, '2025-01-20');


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
    ('Manage Insurance Price List', 'Manage Insurance Price List'),
    ('Manage Duration', 'Manage Duration');

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
    (1, 10, 1), (1, 10, 2), (1, 10, 3), (1, 10, 4),
    (1, 11, 1), (1, 11, 2), (1, 11, 3), (1, 11, 4),

    -- Customers
    (2, 1, 1), (2, 1, 2), (2, 1, 3), 
    (2, 2, 1), (2, 2, 2), (2, 2, 3), (2, 2, 4), 
    (2, 4, 1), (2, 4, 2), (2, 4, 3), (2, 4, 4), 
    (2, 7, 1), (2, 7, 3), (2, 7, 5), (2, 7, 6),
    (2, 8, 1), (2, 8, 2), (2, 8, 3), (2, 8, 4), 
    (2, 9, 1), (2, 9, 3), (2, 9, 5), (2, 9, 6), 
    
    -- Employees
    (3, 3, 1), (3, 3, 2), (3, 3, 3), (3, 3, 4), 
    (3, 4, 1), (3, 3, 3),
    (3, 5, 1), (3, 5, 2), (3, 5, 3), (3, 5, 4), 
    (3, 6, 1), (3, 6, 2), (3, 6, 3), (3, 6, 4), 
    (3, 7, 1), (3, 7, 2), (3, 7, 3), (3, 7, 4), (3, 7, 5), (3, 7, 6),
    (3, 8, 1), (3, 8, 3),
    (3, 9, 1), (3, 9, 2), (3, 9, 3), (3, 9, 4), (3, 9, 5), (3, 9, 6),
    (3, 10, 1), (3, 10, 2), (3, 10, 3), (3, 10, 4), 
    (3, 11, 1), (3, 11, 2), (3, 11, 3), (3, 11, 4);
