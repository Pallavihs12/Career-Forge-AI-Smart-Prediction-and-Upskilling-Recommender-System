-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Apr 25, 2025 at 02:18 PM
-- Server version: 8.3.0
-- PHP Version: 8.3.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `skillgap_2025`
--

-- --------------------------------------------------------

--
-- Table structure for table `skillgap_2025_data`
--

DROP TABLE IF EXISTS `skillgap_2025_data`;
CREATE TABLE IF NOT EXISTS `skillgap_2025_data` (
  `id` int NOT NULL AUTO_INCREMENT,
  `uid` varchar(255) NOT NULL,
  `user` varchar(255) NOT NULL,
  `username` varchar(255) NOT NULL,
  `directory` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `skillgap_2025_questions`
--

DROP TABLE IF EXISTS `skillgap_2025_questions`;
CREATE TABLE IF NOT EXISTS `skillgap_2025_questions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `uid` varchar(255) NOT NULL,
  `question_no` int NOT NULL,
  `question_text` varchar(255) NOT NULL,
  `option_a` varchar(255) NOT NULL,
  `option_b` varchar(255) NOT NULL,
  `option_c` varchar(255) NOT NULL,
  `option_d` varchar(255) NOT NULL,
  `correct_answer` varchar(255) NOT NULL,
  `segment` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uid` (`uid`)
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `skillgap_2025_questions`
--

INSERT INTO `skillgap_2025_questions` (`id`, `uid`, `question_no`, `question_text`, `option_a`, `option_b`, `option_c`, `option_d`, `correct_answer`, `segment`) VALUES
(1, 'uidA1b2C3d4E5f', 1, 'What is 7 + 6?', '12', '13', '14', '15', '13', 'Maths'),
(2, 'uidG7h8I9j0K1l', 2, 'What is the square root of 81?', '8', '9', '10', '11', '9', 'Maths'),
(3, 'uidM3n4O5p6Q7r', 3, 'What is the value of ? (pi)?', '3.14', '2.71', '1.62', '3.41', '3.14', 'Maths'),
(4, 'uidS9t0U1v2W3x', 4, 'Solve: 2x = 10', 'x=3', 'x=4', 'x=5', 'x=6', 'x=5', 'Maths'),
(5, 'uidY5z6A7b8C9d', 5, 'What is 25% of 200?', '25', '50', '75', '100', '50', 'Maths'),
(6, 'uidE1f2G3h4I5j', 6, 'What is 12²', '124', '144', '134', '154', '144', 'Maths'),
(7, 'uidK7l8M9n0O1p', 7, 'If angle A = 90°, it is called?', 'Acute', 'Right', 'Obtuse', 'Reflex', 'Right', 'Maths'),
(8, 'uidQ3r4S5t6U7v', 8, 'What is the area of a rectangle (l=10, b=5)?', '50', '25', '30', '60', '50', 'Maths'),
(9, 'uidW9x0Y1z2A3b', 9, 'What comes next in the sequence: 2, 4, 8, 16...?', '18', '24', '32', '36', '32', 'Maths'),
(10, 'uidC5d6E7f8G9h', 10, 'What is 100 ÷ 4?', '20', '25', '30', '35', '25', 'Maths'),
(11, 'uidI1j2K3l4M5n', 11, 'What is the next number: 2, 4, 8, 16, ___?', '18', '24', '32', '36', '32', 'Aptitude'),
(12, 'uidO7p8Q9r0S1t', 12, 'If a train travels 90 km in 3 hours, what is the speed?', '25 km/h', '30 km/h', '35 km/h', '40 km/h', '30km/h', 'Aptitude'),
(13, 'uidU3v4W5x6Y7z', 13, 'What is the opposite of \"generous\"?', 'Kind', 'Mean', 'Brave', 'Loyal', 'Mean', 'Aptitude'),
(14, 'uidA9b0C1d2E3f', 14, '5 men can complete a task in 12 days. How many days for 10 men?', '6', '7', '8', '9', '6', 'Aptitude'),
(15, 'uidG5h6I7j8K9l', 15, 'Find the missing number: 3, 6, 9, __, 15', '10', '11', '12', '13', '12', 'Aptitude'),
(16, 'uidM1n2O3p4Q5r', 16, 'A sells a pen for ?120 making a profit of 20%. What was the cost price?', '?90', '?100', '?110', '?80', '? 100.00', 'Aptitude'),
(17, 'uidS7t8U9v0W1x', 17, 'What comes next: Z, X, V, T, ___?', 'R', 'Q', 'S', 'U', 'R', 'Aptitude'),
(18, 'uidY3z4A5b6C7d', 18, 'If the area of a square is 64, what is the side length?', '6', '7', '8', '9', '8', 'Aptitude'),
(19, 'uidE9f0G1h2I3j', 19, 'What is 75% of 160?', '100', '110', '120', '130', '120', 'Aptitude'),
(20, 'uidK5l6M7n8O9p', 20, 'Synonym of \'Brief\'?', 'Long', 'Quick', 'Short', 'Wide', 'Short', 'Aptitude'),
(21, 'uidQ1r2S3t4U5v', 21, 'Which of the following is a correct C++ comment?', '# This is a comment', '// This is a comment', '<!-- Comment -->', '%% comment', '// This is a comment', 'C++'),
(22, 'uidW7x8Y9z0A1b', 22, 'Who developed C++?', 'Dennis Ritchie', 'Bjarne Stroustrup', 'James Gosling', 'Guido van Rossum', 'Bjarne Stroustrup', 'C++'),
(23, 'uidC3d4E5f6G7h', 23, 'What is the correct file extension for C++ files?', '.c', '.cpp', '.cp', '.class', '.cpp', 'C++'),
(24, 'uidI9j0K1l2M3n', 24, 'Which header file is required for cout?', 'stdio.h', 'iostream', 'conio.h', 'string.h', 'iostream', 'C++'),
(25, 'uidO5p6Q7r8S9t', 25, 'What is the output of: cout << 5 + 2 * 3;', '21', '11', '17', '25', '11', 'C++'),
(26, 'uidU1v2W3x4Y5z', 26, 'Which of the following is a valid variable name in C++?', '1var', 'my-var', '_total', 'class', 'my-var', 'C++'),
(27, 'uidA7b8C9d0E1f', 27, 'What does OOP stand for?', 'Object Oriented Programming', 'Order of Operation Processing', 'Operator Overloaded Program', 'None', 'Order of Operation Processing', 'C++'),
(28, 'uidG3h4I5j6K7l', 28, 'Which keyword is used to define a class in C++?', 'struct', 'object', 'class', 'define', 'object', 'C++'),
(29, 'uidM9n0O1p2Q3r', 29, 'What is a constructor?', 'Function with return type', 'Special function to initialize objects', 'Destructor', 'None', 'Special function to initialize objects', 'C++'),
(30, 'uidS5t6U7v8W9x', 30, 'Which operator is used to access members of a class using a pointer?', '.', '->', '*', '&', '->', 'C++'),
(31, 'uidY1z2A3b4C5d', 31, 'What does CPU stand for?', 'Central Process Unit', 'Central Processing Unit', 'Computer Process Utility', 'Central Program Unit', 'Central Processing Unit', 'Computer Science'),
(32, 'uidE7f8G9h0I1j', 32, 'Which of these is an input device?', 'Printer', 'Monitor', 'Keyboard', 'Speaker', 'Keyboard', 'Computer Science'),
(33, 'uidK3l4M5n6O7p', 33, 'What is the binary of 5?', '110', '101', '111', '100', '101', 'Computer Science'),
(34, 'uidQ9r0S1t2U3v', 34, 'What does HTML stand for?', 'HyperText Markup Language', 'HighText Mark Language', 'HyperText Markdown Language', 'HyperTransfer Markup Language', 'HyperText Markup Language', 'Computer Science'),
(35, 'uidW5x6Y7z8A9b', 35, 'RAM is used for?', 'Permanent Storage', 'Processing', 'Temporary Storage', 'Display', 'Temporary Storage', 'Computer Science'),
(36, 'uidC1d2E3f4G5h', 36, 'Which language is used to style web pages?', 'HTML', 'jQuery', 'CSS', 'XML', 'CSS', 'Computer Science'),
(37, 'uidI7j8K9l0M1n', 37, 'What is the full form of URL?', 'Uniform Resource Locator', 'Uniform Reference Locator', 'Universal Resource Link', 'Uniform Register Link', 'Uniform Resource Locator', 'Computer Science'),
(38, 'uidO3p4Q5r6S7t', 38, 'Which company created Windows OS?', 'Apple', 'IBM', 'Microsoft', 'Google', 'Microsoft', 'Computer Science'),
(39, 'uidU9v0W1x2Y3z', 39, 'What is the brain of the computer?', 'Monitor', 'CPU', 'RAM', 'Hard Disk', 'CPU', 'Computer Science'),
(40, 'uidA5b6C7d8E9f', 40, 'What is a virus in computers?', 'A game', 'A memory device', 'A malware program', 'A browser', 'A malware program', 'Computer Science');

-- --------------------------------------------------------

--
-- Table structure for table `skillgap_2025_result`
--

DROP TABLE IF EXISTS `skillgap_2025_result`;
CREATE TABLE IF NOT EXISTS `skillgap_2025_result` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_uid` varchar(255) NOT NULL,
  `segment` varchar(255) NOT NULL,
  `score` int NOT NULL,
  `timestamp` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `user_uid` (`user_uid`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `skillgap_2025_resultitems`
--

DROP TABLE IF EXISTS `skillgap_2025_resultitems`;
CREATE TABLE IF NOT EXISTS `skillgap_2025_resultitems` (
  `id` int NOT NULL AUTO_INCREMENT,
  `result_id` int NOT NULL,
  `question_uid` varchar(255) NOT NULL,
  `correct_answer` varchar(255) NOT NULL,
  `user_answer` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `result_id` (`result_id`),
  KEY `question_uid` (`question_uid`)
) ENGINE=InnoDB AUTO_INCREMENT=181 DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `skillgap_2025_user`
--

DROP TABLE IF EXISTS `skillgap_2025_user`;
CREATE TABLE IF NOT EXISTS `skillgap_2025_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `uid` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `phone` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uid` (`uid`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `skillgap_2025_result`
--
ALTER TABLE `skillgap_2025_result`
  ADD CONSTRAINT `skillgap_2025_result_ibfk_1` FOREIGN KEY (`user_uid`) REFERENCES `skillgap_2025_user` (`uid`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `skillgap_2025_resultitems`
--
ALTER TABLE `skillgap_2025_resultitems`
  ADD CONSTRAINT `skillgap_2025_resultitems_ibfk_1` FOREIGN KEY (`result_id`) REFERENCES `skillgap_2025_result` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `skillgap_2025_resultitems_ibfk_2` FOREIGN KEY (`question_uid`) REFERENCES `skillgap_2025_questions` (`uid`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
