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

CREATE TABLE Groups (
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
    FOREIGN KEY (InsuranceCategoryID) REFERENCES InsuranceCategories(ID),
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
    FOREIGN KEY (GroupID) REFERENCES Groups(ID),
    FOREIGN KEY (FunctionID) REFERENCES Functions(ID),
    FOREIGN KEY (ActionID) REFERENCES Actions(ID)
);

-- sample data 
-- Customers
INSERT INTO Customers (Username, Password, Fullname, Address, Email, Phone)
VALUES 
('customer1','123456','Nguyen Van A','123 Street, Hanoi','a@example.com','0912345678'),
('customer2','123456','Tran Thi B','456 Street, HCMC','b@example.com','0987654321');

-- VehicleTypes
INSERT INTO VehicleTypes (Name, Fee, Description, MaxClaimableAmount)
VALUES
('Sedan', 0.05, 'Standard sedan car', 500000000),
('SUV', 0.07, 'Sport Utility Vehicle', 800000000);

-- Vehicles
INSERT INTO Vehicles (Name, CustomerID, Model, VehicleTypeID, PurchasePrice, BodyNumber, EngineNumber, Number, RegistrationDate)
VALUES
('Car A',1,'Model X',1,400000000,'B12345','E12345','30A-11111','2022-01-01'),
('Car B',2,'Model Y',2,700000000,'B67890','E67890','30B-22222','2023-03-01');

-- InsuranceCategories
INSERT INTO InsuranceCategories (Name, Description)
VALUES
('Bảo hiểm toàn bộ','Comprehensive insurance');

-- Duration
INSERT INTO Duration (Months)
VALUES
(12),(60),(120),(180);

-- InsurancePriceList (based on your image)
INSERT INTO InsurancePriceList (InsuranceCategoryID, DurationID, Years, Rate)
VALUES
(1,1,5,5),(1,2,10,6),(1,3,15,7),
(1,1,5,8),(1,2,10,10),(1,3,15,12);

-- Expenses
INSERT INTO Expenses (Content, Amount, Date)
VALUES
('Office rent', 5000000, '2025-01-01'),
('Electricity', 1200000, '2025-01-15'),
('Internet', 800000, '2025-01-20');
