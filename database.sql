-- Database 
CREATE DATABASE IF NOT EXISTS VehicleInsuranceDB;
USE VehicleInsuranceDB;

-- Groups
CREATE TABLE GroupsUsers (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    GroupName VARCHAR(100),
    Description TEXT
);

-- Employees
CREATE TABLE Employees (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Username VARCHAR(50) UNIQUE,
    Fullname VARCHAR(100),
    Email VARCHAR(100) UNIQUE,
    Phone VARCHAR(20) UNIQUE,
    Password VARCHAR(255),
    GroupID INT,
    FOREIGN KEY (GroupID) REFERENCES GroupsUsers(ID)
);

-- Customers
CREATE TABLE Customers (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Fullname VARCHAR(100),
    Address TEXT,
    Email VARCHAR(100) UNIQUE,
    Phone VARCHAR(20) UNIQUE,
    Username VARCHAR(50) UNIQUE,
    Password VARCHAR(255)
);

-- VehicleTypes
CREATE TABLE VehicleTypes (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(50),
    Fee DECIMAL(15,2),
    Description TEXT,
    MaxClaimableAmount DECIMAL(15,2)
);

-- Vehicles
CREATE TABLE Vehicles (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(100),
    CustomerID INT,
    Model VARCHAR(50),
    TypeID INT,
    Rate DECIMAL(15,2),
    BodyNumber VARCHAR(50),
    EngineNumber VARCHAR(50),
    Number VARCHAR(20),
    RegistrationDate DATE,
    FOREIGN KEY (CustomerID) REFERENCES Customers(ID),
    FOREIGN KEY (TypeID) REFERENCES VehicleTypes(ID)
);

-- Depreciation
CREATE TABLE Depreciation (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Rate DECIMAL(5,2)
);

-- InsuranceCategories
CREATE TABLE InsuranceCategories (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(100),
    Fee DECIMAL(15,2),
    Rate DECIMAL(5,2),
    Type VARCHAR(50),
    Description TEXT
);

-- Estimates
CREATE TABLE Estimates (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    VehicleID INT,
    InsuranceCategoryID INT,
    FOREIGN KEY (VehicleID) REFERENCES Vehicles(ID),
    FOREIGN KEY (InsuranceCategoryID) REFERENCES InsuranceCategories(ID)
);

-- Discounts
CREATE TABLE Discounts (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(100),
    Rate DECIMAL(5,2),
    Description TEXT
);

-- EstimateDiscount
CREATE TABLE EstimateDiscount (
    DiscountID INT,
    EstimateID INT,
    PRIMARY KEY (DiscountID, EstimateID),
    FOREIGN KEY (DiscountID) REFERENCES Discounts(ID),
    FOREIGN KEY (EstimateID) REFERENCES Estimates(ID)
);

-- Contracts
CREATE TABLE Contracts (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    ContractNo VARCHAR(50) UNIQUE,
    EstimateID INT,
    Duration INT,
    Fee DECIMAL(15,2),
    Deductible DECIMAL(15,2),
    UsageTime INT,
    MaxClaimAmount DECIMAL(15,2),
    IdentifyNumber VARCHAR(50),
    IdentifyAddress VARCHAR(255),
    IdentifyDate DATE,
    IssuingAuthority VARCHAR(100),
    TaxID VARCHAR(50),
    CreatedBy INT,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    StartDate DATE,
    Status VARCHAR(50),
    FOREIGN KEY (EstimateID) REFERENCES Estimates(ID),
    FOREIGN KEY (CreatedBy) REFERENCES Employees(ID),
    FOREIGN KEY (UsageTime) REFERENCES Depreciation(ID)
);

-- Expenses
CREATE TABLE Expenses (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Content TEXT,
    Amount DECIMAL(15,2),
    Date DATE
);

-- RequestClaims
CREATE TABLE RequestClaims (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    ContractID INT,
    Place VARCHAR(255),
    Date DATE,
    FOREIGN KEY (ContractID) REFERENCES Contracts(ID)
);

-- Claims
CREATE TABLE Claims (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    ClaimNo VARCHAR(50) UNIQUE,
    RequestClaimID INT,
    DamageAmount DECIMAL(15,2),
    Deductible DECIMAL(15,2),
    ClaimAmount DECIMAL(15,2),
    FOREIGN KEY (RequestClaimID) REFERENCES RequestClaims(ID)
);

-- Reduction
CREATE TABLE Reduction (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(100),
    Rate DECIMAL(5,2),
    Description TEXT
);

-- ClaimReduction
CREATE TABLE ClaimReduction (
    ClaimID INT,
    ReductionID INT,
    PRIMARY KEY (ClaimID, ReductionID),
    FOREIGN KEY (ClaimID) REFERENCES Claims(ID),
    FOREIGN KEY (ReductionID) REFERENCES Reduction(ID)
);

-- Functions
CREATE TABLE Functions (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    FunctionName VARCHAR(100),
    Description TEXT
);

-- Actions
CREATE TABLE Actions (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    ActionName VARCHAR(100),
    Description TEXT
);

-- GroupsFunctionsActions
CREATE TABLE GroupsFunctionsActions (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    GroupID INT NOT NULL,
    FunctionID INT NOT NULL,
    ActionID INT NOT NULL,
    FOREIGN KEY (GroupID) REFERENCES GroupsUsers(ID),
    FOREIGN KEY (FunctionID) REFERENCES Functions(ID),
    FOREIGN KEY (ActionID) REFERENCES Actions(ID)
);


-- Sample data
USE VehicleInsuranceDB;

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

INSERT INTO Functions (FunctionName, Description)
VALUES 
    ('Manage Customers', 'Manage Customers'),
    ('Manage Vehicles', 'Manage Vehicles'),
    ('Manage Vehicle types', 'Manage Vehicle types'),
    ('Manage Estimates', 'Manage Estimates'),
    ('Manage Discounts', 'Manage Discounts'),
    ('Manage Insurance Categories', 'Manage Insurance Categories'),
    ('Manage Contracts', 'Manage Contracts'),
    ('Manage Claim requests', 'Manage Claim requests'),
    ('Manage Claims', 'Manage Claims'),
    ('Manage Reductions', 'Manage Reductions'),
    ('Manage Expenses', 'Manage Expenses'),
    ('Manage Employees', 'Manage Employees'),
    ('Manage Groups users', 'Manage Groups users');

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
    (1, 12, 1), (1, 12, 2), (1, 12, 3), (1, 12, 4), 
    (1, 13, 1), (1, 13, 2), (1, 13, 3), (1, 13, 4),

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
    (3, 11, 1), (3, 11, 2), (3, 11, 3), (3, 11, 4), 
    (3, 12, 1), (3, 12, 2), (3, 12, 3);