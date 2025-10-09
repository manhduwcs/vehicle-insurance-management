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
    DeductibleValue DECIMAL(15,2),
    DeductibleAddon DECIMAL(15,2),
    ActualValue DECIMAL(15,2),
    ActualPremium DECIMAL(15,2),
    FixedDeduction DECIMAL(15,2),
    MaxPersonCompensation DECIMAL(15,2),
    AvailablePersonCompensation DECIMAL(15,2),
    AvailablePropertyCompensation DECIMAL(15,2),
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
    CategoryID INT,
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
    FOREIGN KEY (ContractID) REFERENCES Contracts(ID),
    FOREIGN KEY (CategoryID) REFERENCES InsuranceCategories(ID)
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
INSERT INTO Customers (Username, Password, Fullname, Address, Email, Phone)
VALUES 
('nguyenvana', '123456', 'Nguyễn Văn An', '12 Nguyễn Trãi, Quận 1, TP. Hồ Chí Minh', 'an.nguyen@example.com', '0903123456'),
('tranthibich', '123456', 'Trần Thị Bích', '45 Cầu Giấy, Quận Cầu Giấy, Hà Nội', 'bich.tran@example.com', '0987234567'),
('leminhduc', '123456', 'Lê Minh Đức', '89 Lê Lợi, TP. Đà Nẵng', 'duc.le@example.com', '0934567890'),
('phamthanhha', '123456', 'Phạm Thanh Hà', '21 Nguyễn Huệ, TP. Huế', 'ha.pham@example.com', '0976543210'),
('danghoangnam', '123456', 'Đặng Hoàng Nam', '5 Lý Thường Kiệt, TP. Hải Phòng', 'nam.dang@example.com', '0912789345');

-- VehicleTypes
INSERT INTO VehicleTypes (Name, Fee, Description, MaxPersonalCompensation, MaxPropertyCompensation)
VALUES
-- Xe máy
('Xe máy dưới 50cc', 55000, 'Xe mô tô dung tích dưới 50cc', 70000000, 30000000),
('Xe máy trên 50cc', 60000, 'Xe mô tô dung tích trên 50cc', 80000000, 40000000),

-- Ô tô chở người
('Ô tô dưới 6 chỗ', 437000, 'Xe ô tô chở người dưới 6 chỗ (không kinh doanh)', 120000000, 70000000),
('Ô tô từ 6 đến 11 chỗ', 794000, 'Xe ô tô chở người từ 6–11 chỗ ngồi', 150000000, 90000000),
('Ô tô kinh doanh vận tải dưới 6 chỗ', 756000, 'Xe ô tô kinh doanh vận tải dưới 6 chỗ', 180000000, 100000000),

-- Ô tô tải, đầu kéo
('Ô tô tải dưới 3.5 tấn', 853000, 'Xe tải có trọng tải dưới 3.5 tấn', 200000000, 150000000),
('Ô tô tải từ 3.5 đến 7 tấn', 1660000, 'Xe tải trọng tải từ 3.5 đến 7 tấn', 250000000, 200000000),
('Ô tô đầu kéo', 1826000, 'Đầu kéo sơ-mi rơ-moóc', 300000000, 250000000);

-- Vehicles
INSERT INTO Vehicles (Name, CustomerID, Model, VehicleTypeID, PurchasePrice, BodyNumber, EngineNumber, Number, RegistrationDate)
VALUES
('Toyota Vios', 1, 'Vios G 2021', 1, 560000000, 'TH12345', 'EN98765', '30A-45678', '2022-05-12'),
('Honda City', 2, 'City RS 2022', 1, 620000000, 'TH54321', 'EN12345', '30B-56789', '2023-02-10'),
('Yamaha Exciter', 3, 'Exciter 155', 2, 48000000, 'TH88888', 'EN77777', '29E1-12345', '2023-06-20'),
('Kia K200', 4, 'K200 1.9 Tấn', 3, 465000000, 'TH99999', 'EN66666', '29C-88888', '2021-11-05'),
('Mazda CX-5', 5, 'CX-5 Premium 2023', 1, 850000000, 'TH11223', 'EN33445', '30F-99999', '2023-09-01');

-- InsuranceCategories
INSERT INTO InsuranceCategories (Name, Description)
VALUES
('Bảo hiểm TNDS bắt buộc', 'Bảo hiểm bắt buộc theo quy định, chi trả thiệt hại cho bên thứ ba về người và tài sản.'),
('Bảo hiểm vật chất xe', 'Bảo hiểm toàn diện cho xe trước các rủi ro va chạm, cháy nổ, thiên tai hoặc mất cắp toàn bộ.'),
('Bảo hiểm mất cắp bộ phận', 'Chi trả khi xe bị mất phụ tùng, linh kiện riêng lẻ như gương, đèn, bánh xe...'),
('Bảo hiểm thân vỏ', 'Chỉ bảo hiểm phần thân vỏ xe khi bị trầy xước, móp méo, va chạm nhẹ.'),
('Bảo hiểm thủy kích', 'Chi trả thiệt hại khi xe bị ngập nước, thủy kích làm hỏng động cơ.'),
('Bảo hiểm cháy nổ', 'Chi trả thiệt hại do cháy, nổ không kiểm soát được trong quá trình vận hành hoặc đỗ xe.'),
('Bảo hiểm thiên tai', 'Chi trả thiệt hại do thiên tai như bão, lũ, sạt lở, mưa đá gây ra cho xe.'),
('Bảo hiểm mất toàn bộ xe', 'Chi trả khi xe bị cướp, mất trộm toàn bộ hoặc hư hỏng không thể phục hồi.'),
('Bảo hiểm tai nạn người ngồi trên xe', 'Bồi thường cho người lái và hành khách khi bị thương hoặc tử vong do tai nạn giao thông.');

-- Duration
INSERT INTO Duration (Months)
VALUES
(12),
(24),
(36);

-- InsurancePriceList (based on your image)
INSERT INTO InsurancePriceList (InsuranceCategoryID, DurationID, Years, Rate)
VALUES
-- TNDS bắt buộc
(1, 1, 5, 5), (1, 2, 10, 6), (1, 3, 15, 7),

-- Tai nạn người ngồi trên xe
(2, 1, 5, 3), (2, 2, 10, 4), (2, 3, 15, 5),

-- Vật chất xe
(3, 1, 5, 10), (3, 2, 10, 12), (3, 3, 15, 14),

-- Mất cắp bộ phận
(4, 1, 5, 8), (4, 2, 10, 9), (4, 3, 15, 10),

-- Thủy kích
(5, 1, 5, 6), (5, 2, 10, 8), (5, 3, 15, 10),

-- Cháy nổ xe
(6, 1, 5, 7), (6, 2, 10, 9), (6, 3, 15, 11);

-- Expenses
INSERT INTO Expenses (Content, Amount, Date)
VALUES
('Thuê văn phòng', 5000000, '2025-01-01'),
('Tiền điện', 1200000, '2025-01-15'),
('Tiền internet', 800000, '2025-01-20'),
('Bảo trì hệ thống máy tính', 2500000, '2025-02-05'),
('Chi phí quảng cáo trực tuyến', 3500000, '2025-02-10'),
('Mua văn phòng phẩm', 950000, '2025-02-18'),
('Tiền nước', 600000, '2025-03-01'),
('Chi phí vệ sinh tòa nhà', 1000000, '2025-03-10'),
('Chi phí bảo dưỡng xe công ty', 4200000, '2025-03-25');

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
