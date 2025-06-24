-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Máy chủ: 127.0.0.1
-- Thời gian đã tạo: Th5 06, 2025 lúc 08:18 PM
-- Phiên bản máy phục vụ: 10.4.32-MariaDB
-- Phiên bản PHP: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Cơ sở dữ liệu: `project001`
--

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `employees`
--

CREATE TABLE `employees` (
  `id` int(11) NOT NULL,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `avatar` varchar(255) NOT NULL,
  `role` varchar(255) NOT NULL,
  `shiftwork` varchar(255) NOT NULL,
  `start` time NOT NULL,
  `end` time NOT NULL,
  `note` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Đang đổ dữ liệu cho bảng `employees`
--

INSERT INTO `employees` (`id`, `username`, `password`, `name`, `email`, `avatar`, `role`, `shiftwork`, `start`, `end`, `note`) VALUES
(0, 'huy132004', 'huy132004', 'Nguyễn Quang Huy', 'huy0132004@gmail.com', 'image\\huy.jpg', 'Bảo vệ ', 'Ca sáng', '00:06:00', '00:14:00', 'Tôi cần ai đó đi hộ ngày mai vì tôi về quê đi ăn đám cưới');

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `monthly_pass`
--

CREATE TABLE `monthly_pass` (
  `id` int(11) NOT NULL,
  `vehicle_type` varchar(255) NOT NULL,
  `license_plate_number` varchar(255) NOT NULL,
  `expired_date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Đang đổ dữ liệu cho bảng `monthly_pass`
--

INSERT INTO `monthly_pass` (`id`, `vehicle_type`, `license_plate_number`, `expired_date`) VALUES
(1, 'Xe máy', '36B7-82608', '2025-10-31'),
(2, 'Xe ô tô', '36B6-42352', '2025-09-30'),
(5, 'Xe máy', '30B2-38493', '2025-08-31'),
(6, 'Xe máy', '29Y3-03658', '2025-06-30');

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `ticket_types`
--

CREATE TABLE `ticket_types` (
  `id` int(11) NOT NULL,
  `vehicle_type` varchar(255) NOT NULL,
  `time` varchar(255) NOT NULL,
  `start` varchar(255) NOT NULL,
  `end` varchar(255) NOT NULL,
  `ticket_type` varchar(255) NOT NULL,
  `price` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Đang đổ dữ liệu cho bảng `ticket_types`
--

INSERT INTO `ticket_types` (`id`, `vehicle_type`, `time`, `start`, `end`, `ticket_type`, `price`) VALUES
(678, 'Xe máy', 'Tháng', '01', '31', 'Vé tháng', 100000),
(679, 'Xe ô tô', 'Tháng', '01', '31', 'Vé tháng', 500000),
(680, 'Xe máy điện', 'Tháng', '01', '31', 'Vé tháng', 80000),
(681, 'Xe máy', 'Ngày', '06:00', '17:59', 'Vé lượt', 5000),
(682, 'Xe ô tô', 'Ngày', '06:00', '17:59', 'Vé lượt', 25000),
(683, 'Xe máy điện', 'Ngày', '06:00', '17:59', 'Vé lượt', 4000),
(684, 'Xe máy', 'Đêm', '18:00', '05:59', 'Vé lượt', 15000),
(685, 'Xe ô tô', 'Đêm', '18:00', '05:59', 'Vé lượt', 75000),
(686, 'Xe máy điện', 'Đêm', '18:00', '05:59', 'Vé lượt', 12000);

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `time_types`
--

CREATE TABLE `time_types` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `start` varchar(255) NOT NULL,
  `end` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Đang đổ dữ liệu cho bảng `time_types`
--

INSERT INTO `time_types` (`id`, `name`, `start`, `end`) VALUES
(2, 'Tháng', '01', '31'),
(3, 'Ngày', '06:00', '17:59'),
(4, 'Đêm', '18:00', '05:59');

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `vehicles`
--

CREATE TABLE `vehicles` (
  `id` int(11) NOT NULL,
  `type` varchar(255) NOT NULL,
  `license_plate_number` varchar(255) NOT NULL,
  `ticket_type` varchar(255) NOT NULL,
  `time` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Đang đổ dữ liệu cho bảng `vehicles`
--

INSERT INTO `vehicles` (`id`, `type`, `license_plate_number`, `ticket_type`, `time`) VALUES
(58, 'Xe máy điện', '29MĐ1-01353', 'Vé lượt', '2025-05-06 13:19:07'),
(64, 'Xe máy', '89E1-18896', 'Vé lượt', '2025-05-06 14:06:30'),
(66, 'Ô tô', '30G-49344', 'Vé lượt', '2025-05-06 14:30:55'),
(70, 'Xe máy', '29A1-08688', 'Vé lượt', '2025-05-06 20:21:31'),
(72, 'Xe máy', '29Y3-03658', 'Vé tháng', '2025-05-06 21:44:15');

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `vehicle_types`
--

CREATE TABLE `vehicle_types` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Đang đổ dữ liệu cho bảng `vehicle_types`
--

INSERT INTO `vehicle_types` (`id`, `name`) VALUES
(1, 'Xe máy'),
(2, 'Xe ô tô'),
(16, 'Xe máy điện');

--
-- Chỉ mục cho các bảng đã đổ
--

--
-- Chỉ mục cho bảng `employees`
--
ALTER TABLE `employees`
  ADD PRIMARY KEY (`id`);

--
-- Chỉ mục cho bảng `monthly_pass`
--
ALTER TABLE `monthly_pass`
  ADD PRIMARY KEY (`id`);

--
-- Chỉ mục cho bảng `ticket_types`
--
ALTER TABLE `ticket_types`
  ADD PRIMARY KEY (`id`);

--
-- Chỉ mục cho bảng `time_types`
--
ALTER TABLE `time_types`
  ADD PRIMARY KEY (`id`);

--
-- Chỉ mục cho bảng `vehicles`
--
ALTER TABLE `vehicles`
  ADD PRIMARY KEY (`id`);

--
-- Chỉ mục cho bảng `vehicle_types`
--
ALTER TABLE `vehicle_types`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT cho các bảng đã đổ
--

--
-- AUTO_INCREMENT cho bảng `employees`
--
ALTER TABLE `employees`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT cho bảng `monthly_pass`
--
ALTER TABLE `monthly_pass`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT cho bảng `ticket_types`
--
ALTER TABLE `ticket_types`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=687;

--
-- AUTO_INCREMENT cho bảng `time_types`
--
ALTER TABLE `time_types`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT cho bảng `vehicles`
--
ALTER TABLE `vehicles`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=73;

--
-- AUTO_INCREMENT cho bảng `vehicle_types`
--
ALTER TABLE `vehicle_types`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
