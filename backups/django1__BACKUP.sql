-- phpMyAdmin SQL Dump
-- version 5.2.3
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Nov 23, 2025 at 09:02 AM
-- Server version: 8.4.7
-- PHP Version: 8.4.14

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `django1`
--
CREATE DATABASE IF NOT EXISTS `django1` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_bin;
USE `django1`;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group`
--
-- Creation: Oct 28, 2025 at 03:02 AM
--

CREATE TABLE `auth_group` (
  `id` int NOT NULL,
  `name` varchar(150) COLLATE utf8mb4_bin NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group_permissions`
--
-- Creation: Oct 28, 2025 at 03:02 AM
--

CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

-- --------------------------------------------------------

--
-- Table structure for table `auth_permission`
--
-- Creation: Oct 28, 2025 at 03:02 AM
-- Last update: Nov 09, 2025 at 09:54 AM
--

CREATE TABLE `auth_permission` (
  `id` int NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_bin NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) COLLATE utf8mb4_bin NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

--
-- Dumping data for table `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 2, 'add_permission'),
(6, 'Can change permission', 2, 'change_permission'),
(7, 'Can delete permission', 2, 'delete_permission'),
(8, 'Can view permission', 2, 'view_permission'),
(9, 'Can add group', 3, 'add_group'),
(10, 'Can change group', 3, 'change_group'),
(11, 'Can delete group', 3, 'delete_group'),
(12, 'Can view group', 3, 'view_group'),
(13, 'Can add user', 4, 'add_user'),
(14, 'Can change user', 4, 'change_user'),
(15, 'Can delete user', 4, 'delete_user'),
(16, 'Can view user', 4, 'view_user'),
(17, 'Can add content type', 5, 'add_contenttype'),
(18, 'Can change content type', 5, 'change_contenttype'),
(19, 'Can delete content type', 5, 'delete_contenttype'),
(20, 'Can view content type', 5, 'view_contenttype'),
(21, 'Can add session', 6, 'add_session'),
(22, 'Can change session', 6, 'change_session'),
(23, 'Can delete session', 6, 'delete_session'),
(24, 'Can view session', 6, 'view_session'),
(25, 'Can add task', 7, 'add_task'),
(26, 'Can change task', 7, 'change_task'),
(27, 'Can delete task', 7, 'delete_task'),
(28, 'Can view task', 7, 'view_task'),
(29, 'Can add task deadline', 8, 'add_taskdeadline'),
(30, 'Can change task deadline', 8, 'change_taskdeadline'),
(31, 'Can delete task deadline', 8, 'delete_taskdeadline'),
(32, 'Can view task deadline', 8, 'view_taskdeadline'),
(33, 'Can add task details', 9, 'add_taskdetails'),
(34, 'Can change task details', 9, 'change_taskdetails'),
(35, 'Can delete task details', 9, 'delete_taskdetails'),
(36, 'Can view task details', 9, 'view_taskdetails'),
(37, 'Can add task status', 10, 'add_taskstatus'),
(38, 'Can change task status', 10, 'change_taskstatus'),
(39, 'Can delete task status', 10, 'delete_taskstatus'),
(40, 'Can view task status', 10, 'view_taskstatus'),
(41, 'Can add task user assignment', 11, 'add_taskuserassignment'),
(42, 'Can change task user assignment', 11, 'change_taskuserassignment'),
(43, 'Can delete task user assignment', 11, 'delete_taskuserassignment'),
(44, 'Can view task user assignment', 11, 'view_taskuserassignment'),
(45, 'Can add task watcher', 12, 'add_taskwatcher'),
(46, 'Can change task watcher', 12, 'change_taskwatcher'),
(47, 'Can delete task watcher', 12, 'delete_taskwatcher'),
(48, 'Can view task watcher', 12, 'view_taskwatcher'),
(49, 'Can add assignment', 13, 'add_assignment'),
(50, 'Can change assignment', 13, 'change_assignment'),
(51, 'Can delete assignment', 13, 'delete_assignment'),
(52, 'Can view assignment', 13, 'view_assignment'),
(53, 'Can add deadline', 14, 'add_deadline'),
(54, 'Can change deadline', 14, 'change_deadline'),
(55, 'Can delete deadline', 14, 'delete_deadline'),
(56, 'Can view deadline', 14, 'view_deadline'),
(57, 'Can add details', 15, 'add_details'),
(58, 'Can change details', 15, 'change_details'),
(59, 'Can delete details', 15, 'delete_details'),
(60, 'Can view details', 15, 'view_details'),
(61, 'Can add status', 16, 'add_status'),
(62, 'Can change status', 16, 'change_status'),
(63, 'Can delete status', 16, 'delete_status'),
(64, 'Can view status', 16, 'view_status'),
(65, 'Can add visibility', 17, 'add_visibility'),
(66, 'Can change visibility', 17, 'change_visibility'),
(67, 'Can delete visibility', 17, 'delete_visibility'),
(68, 'Can view visibility', 17, 'view_visibility'),
(69, 'Can add watcher', 18, 'add_watcher'),
(70, 'Can change watcher', 18, 'change_watcher'),
(71, 'Can delete watcher', 18, 'delete_watcher'),
(72, 'Can view watcher', 18, 'view_watcher');

-- --------------------------------------------------------

--
-- Table structure for table `auth_user`
--
-- Creation: Oct 28, 2025 at 03:02 AM
-- Last update: Nov 21, 2025 at 01:09 PM
--

CREATE TABLE `auth_user` (
  `id` int NOT NULL,
  `password` varchar(128) COLLATE utf8mb4_bin NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) COLLATE utf8mb4_bin NOT NULL,
  `first_name` varchar(150) COLLATE utf8mb4_bin NOT NULL,
  `last_name` varchar(150) COLLATE utf8mb4_bin NOT NULL,
  `email` varchar(254) COLLATE utf8mb4_bin NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

--
-- Dumping data for table `auth_user`
--

INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES
(1, 'pbkdf2_sha256$1000000$KosOAJLdhcnJfIqEbOyRL1$PuJwaGzlXti30uIkZlQv8RIwEKTAXWEXov8d3gu0YS4=', '2025-11-21 13:09:34.753229', 1, 'supeadmin', 'Malaika', 'Ghayyur', 'mustafa@web-dotz.com', 1, 1, '2025-10-28 03:29:10.000000');

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_groups`
--
-- Creation: Oct 28, 2025 at 03:02 AM
--

CREATE TABLE `auth_user_groups` (
  `id` bigint NOT NULL,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_user_permissions`
--
-- Creation: Oct 28, 2025 at 03:02 AM
--

CREATE TABLE `auth_user_user_permissions` (
  `id` bigint NOT NULL,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

--
-- Dumping data for table `auth_user_user_permissions`
--

INSERT INTO `auth_user_user_permissions` (`id`, `user_id`, `permission_id`) VALUES
(1, 1, 1),
(2, 1, 2),
(3, 1, 3),
(4, 1, 4),
(5, 1, 5),
(6, 1, 6),
(7, 1, 7),
(8, 1, 8),
(9, 1, 9),
(10, 1, 10),
(11, 1, 11),
(12, 1, 12),
(13, 1, 13),
(14, 1, 14),
(15, 1, 15),
(16, 1, 16),
(17, 1, 17),
(18, 1, 18),
(19, 1, 19),
(20, 1, 20),
(21, 1, 21),
(22, 1, 22),
(23, 1, 23),
(24, 1, 24);

-- --------------------------------------------------------

--
-- Table structure for table `django_admin_log`
--
-- Creation: Oct 28, 2025 at 03:02 AM
-- Last update: Nov 04, 2025 at 09:13 AM
--

CREATE TABLE `django_admin_log` (
  `id` int NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext COLLATE utf8mb4_bin,
  `object_repr` varchar(200) COLLATE utf8mb4_bin NOT NULL,
  `action_flag` smallint UNSIGNED NOT NULL,
  `change_message` longtext COLLATE utf8mb4_bin NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL
) ;

--
-- Dumping data for table `django_admin_log`
--

INSERT INTO `django_admin_log` (`id`, `action_time`, `object_id`, `object_repr`, `action_flag`, `change_message`, `content_type_id`, `user_id`) VALUES
(1, '2025-10-28 05:16:19.846554', '1', 'supeadmin', 2, '[{\"changed\": {\"fields\": [\"First name\", \"Last name\", \"User permissions\"]}}]', 4, 1),
(2, '2025-11-04 09:11:28.037568', '1', 'Task object (1)', 1, '[{\"added\": {}}]', 7, 1),
(3, '2025-11-04 09:12:41.587240', '1', 'TaskDetails object (1)', 1, '[{\"added\": {}}]', 9, 1),
(4, '2025-11-04 09:13:02.031806', '1', 'TaskStatus object (1)', 1, '[{\"added\": {}}]', 10, 1);

-- --------------------------------------------------------

--
-- Table structure for table `django_content_type`
--
-- Creation: Oct 28, 2025 at 03:02 AM
-- Last update: Nov 09, 2025 at 09:54 AM
--

CREATE TABLE `django_content_type` (
  `id` int NOT NULL,
  `app_label` varchar(100) COLLATE utf8mb4_bin NOT NULL,
  `model` varchar(100) COLLATE utf8mb4_bin NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

--
-- Dumping data for table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(4, 'auth', 'user'),
(5, 'contenttypes', 'contenttype'),
(6, 'sessions', 'session'),
(13, 'tasks', 'assignment'),
(14, 'tasks', 'deadline'),
(15, 'tasks', 'details'),
(16, 'tasks', 'status'),
(7, 'tasks', 'task'),
(8, 'tasks', 'taskdeadline'),
(9, 'tasks', 'taskdetails'),
(10, 'tasks', 'taskstatus'),
(11, 'tasks', 'taskuserassignment'),
(12, 'tasks', 'taskwatcher'),
(17, 'tasks', 'visibility'),
(18, 'tasks', 'watcher');

-- --------------------------------------------------------

--
-- Table structure for table `django_migrations`
--
-- Creation: Oct 28, 2025 at 03:02 AM
-- Last update: Nov 16, 2025 at 01:33 AM
--

CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL,
  `app` varchar(255) COLLATE utf8mb4_bin NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_bin NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

--
-- Dumping data for table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2025-10-28 03:02:43.328969'),
(2, 'auth', '0001_initial', '2025-10-28 03:02:43.505547'),
(3, 'admin', '0001_initial', '2025-10-28 03:02:43.551442'),
(4, 'admin', '0002_logentry_remove_auto_add', '2025-10-28 03:02:43.560137'),
(5, 'admin', '0003_logentry_add_action_flag_choices', '2025-10-28 03:02:43.564208'),
(6, 'contenttypes', '0002_remove_content_type_name', '2025-10-28 03:02:43.594487'),
(7, 'auth', '0002_alter_permission_name_max_length', '2025-10-28 03:02:43.613162'),
(8, 'auth', '0003_alter_user_email_max_length', '2025-10-28 03:02:43.625485'),
(9, 'auth', '0004_alter_user_username_opts', '2025-10-28 03:02:43.629911'),
(10, 'auth', '0005_alter_user_last_login_null', '2025-10-28 03:02:43.649805'),
(11, 'auth', '0006_require_contenttypes_0002', '2025-10-28 03:02:43.650667'),
(12, 'auth', '0007_alter_validators_add_error_messages', '2025-10-28 03:02:43.655609'),
(13, 'auth', '0008_alter_user_username_max_length', '2025-10-28 03:02:43.678626'),
(14, 'auth', '0009_alter_user_last_name_max_length', '2025-10-28 03:02:43.707493'),
(15, 'auth', '0010_alter_group_name_max_length', '2025-10-28 03:02:43.720083'),
(16, 'auth', '0011_update_proxy_permissions', '2025-10-28 03:02:43.725143'),
(17, 'auth', '0012_alter_user_first_name_max_length', '2025-10-28 03:02:43.744807'),
(18, 'sessions', '0001_initial', '2025-10-28 03:02:43.754920'),
(19, 'tasks', '0001_initial', '2025-11-04 08:41:12.912223'),
(20, 'tasks', '0002_alter_task_delete_time_alter_task_update_time_and_more', '2025-11-04 08:41:13.046462'),
(21, 'tasks', '0003_alter_task_create_time_and_more', '2025-11-04 08:46:40.172992'),
(22, 'tasks', '0004_remove_task_deadline', '2025-11-04 08:53:18.201021'),
(23, 'tasks', '0005_alter_task_parent_id', '2025-11-04 09:09:53.207707'),
(24, 'tasks', '0006_remove_taskdetails_task_id_remove_taskstatus_task_id_and_more', '2025-11-09 09:54:05.467103'),
(25, 'tasks', '0007_alter_assignment_managers_alter_deadline_managers_and_more', '2025-11-16 01:33:55.849391'),
(26, 'tasks', '0008_alter_assignment_create_time_and_more', '2025-11-23 09:01:51.303374');

-- --------------------------------------------------------

--
-- Table structure for table `django_session`
--
-- Creation: Oct 28, 2025 at 03:02 AM
-- Last update: Nov 21, 2025 at 01:09 PM
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) COLLATE utf8mb4_bin NOT NULL,
  `session_data` longtext COLLATE utf8mb4_bin NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

--
-- Dumping data for table `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('lrf82yvyxutzhwl21p8mcavkpwdnsfyn', '.eJxVjMEOwiAQRP-FsyFYYEGP3vsNZJcFqRpISnsy_rtt0oMeZ96beYuA61LC2tMcJhZXcRan344wPlPdAT-w3puMrS7zRHJX5EG7HBun1-1w_w4K9rKtL26IOmaizNYMiiyyYqeMiawRDDI6MmhdBsOg0xbAEibQGrT34MXnCwHXODA:1vGCu8:xKW_MoG8pu-lIHI7Q9JJ9H1FgFE_RksLH0oZqKHpmy0', '2025-11-18 09:00:40.719118'),
('m2g6h62iqrj2fsh8nt1k2qwzcptusuet', '.eJxVjMEOwiAQRP-FsyFYYEGP3vsNZJcFqRpISnsy_rtt0oMeZ96beYuA61LC2tMcJhZXcRan344wPlPdAT-w3puMrS7zRHJX5EG7HBun1-1w_w4K9rKtL26IOmaizNYMiiyyYqeMiawRDDI6MmhdBsOg0xbAEibQGrT34MXnCwHXODA:1vMQtK:JQ9uTOxlM4OWm6ixatdvhSe5SVr0Btrpd3s7sHi4X9M', '2025-12-05 13:09:34.754935');

-- --------------------------------------------------------

--
-- Table structure for table `tasks_assignment`
--
-- Creation: Nov 16, 2025 at 01:33 AM
-- Last update: Nov 20, 2025 at 07:48 AM
--

CREATE TABLE `tasks_assignment` (
  `id` bigint NOT NULL,
  `latest` smallint NOT NULL DEFAULT '1',
  `create_time` datetime(6) NOT NULL,
  `delete_time` datetime(6) DEFAULT NULL,
  `assignee_id` int NOT NULL,
  `assignor_id` int NOT NULL,
  `task_id` bigint NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

--
-- Dumping data for table `tasks_assignment`
--

INSERT INTO `tasks_assignment` (`id`, `latest`, `create_time`, `delete_time`, `assignee_id`, `assignor_id`, `task_id`) VALUES
(1, 2, '2025-11-09 04:55:04.000000', '2025-11-20 07:37:59.973544', 1, 1, 1),
(2, 2, '2025-11-17 10:46:14.424241', '2025-11-20 07:48:22.505544', 1, 1, 17),
(3, 1, '2025-11-17 10:58:51.201502', NULL, 1, 1, 18),
(4, 2, '2025-11-17 11:02:19.245589', '2025-11-20 07:10:51.560328', 1, 1, 19),
(5, 2, '2025-11-17 11:08:01.096285', '2025-11-20 07:38:21.739682', 1, 1, 20),
(6, 1, '2025-11-17 11:08:49.108746', NULL, 1, 1, 21),
(7, 1, '2025-11-17 11:09:45.223740', NULL, 1, 1, 22),
(8, 1, '2025-11-17 11:18:27.567403', NULL, 1, 1, 23),
(9, 2, '2025-11-17 12:18:34.435140', '2025-11-19 09:31:57.591927', 1, 1, 24),
(10, 2, '2025-11-17 23:54:28.884615', '2025-11-19 09:00:13.386082', 1, 1, 25),
(11, 1, '2025-11-19 09:00:13.388431', NULL, 1, 1, 25),
(12, 1, '2025-11-19 09:31:57.594777', NULL, 1, 1, 24);

-- --------------------------------------------------------

--
-- Table structure for table `tasks_deadline`
--
-- Creation: Nov 16, 2025 at 01:33 AM
-- Last update: Nov 23, 2025 at 02:57 AM
--

CREATE TABLE `tasks_deadline` (
  `id` bigint NOT NULL,
  `deadline` datetime(6) NOT NULL,
  `latest` smallint NOT NULL DEFAULT '1',
  `create_time` datetime(6) NOT NULL,
  `delete_time` datetime(6) DEFAULT NULL,
  `task_id` bigint NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

--
-- Dumping data for table `tasks_deadline`
--

INSERT INTO `tasks_deadline` (`id`, `deadline`, `latest`, `create_time`, `delete_time`, `task_id`) VALUES
(1, '2025-11-26 05:36:00.000000', 1, '2025-11-17 10:17:33.564621', NULL, 12),
(2, '2025-11-26 05:36:00.000000', 1, '2025-11-17 10:30:05.238738', NULL, 13),
(3, '2025-11-26 05:36:00.000000', 1, '2025-11-17 10:35:29.748404', NULL, 14),
(4, '2025-11-26 05:36:00.000000', 1, '2025-11-17 10:39:02.135078', NULL, 15),
(5, '2025-11-26 05:36:00.000000', 1, '2025-11-17 10:43:09.738333', NULL, 16),
(6, '2025-11-26 05:36:00.000000', 2, '2025-11-17 10:46:14.418957', '2025-11-20 07:48:22.499724', 17),
(7, '2025-11-26 05:36:00.000000', 1, '2025-11-17 10:58:51.192597', NULL, 18),
(8, '2025-11-26 05:36:00.000000', 2, '2025-11-17 11:02:19.240323', '2025-11-20 07:10:51.556695', 19),
(9, '2025-11-26 05:36:00.000000', 2, '2025-11-17 11:08:01.090911', '2025-11-20 02:05:58.473572', 20),
(10, '2025-11-26 05:36:00.000000', 2, '2025-11-17 11:08:49.095819', '2025-11-19 12:51:21.330183', 21),
(11, '2025-11-26 05:36:00.000000', 1, '2025-11-17 11:09:45.216915', NULL, 22),
(12, '2025-11-26 05:36:00.000000', 1, '2025-11-17 11:18:27.556311', NULL, 23),
(13, '2025-11-26 05:36:00.000000', 2, '2025-11-17 12:18:34.429534', '2025-11-19 09:31:57.575810', 24),
(14, '2025-11-26 05:36:00.000000', 2, '2025-11-17 23:54:28.877762', '2025-11-19 09:00:13.371024', 25),
(15, '2025-11-26 05:36:00.000000', 1, '2025-11-19 09:00:13.374362', NULL, 25),
(16, '2025-11-30 05:36:00.000000', 2, '2025-11-19 09:31:57.578150', '2025-11-19 12:44:26.805562', 24),
(17, '2025-11-30 05:36:00.000000', 2, '2025-11-19 12:44:26.808135', '2025-11-23 02:57:22.085616', 24),
(18, '2025-12-01 05:36:00.000000', 1, '2025-11-19 12:51:21.332417', NULL, 21),
(19, '2025-12-06 10:36:00.000000', 2, '2025-11-20 02:05:58.476284', '2025-11-20 02:11:34.327941', 20),
(20, '2025-12-06 15:36:00.000000', 2, '2025-11-20 02:11:34.333156', '2025-11-20 02:22:59.997523', 20),
(21, '2025-12-06 20:36:00.000000', 2, '2025-11-20 02:23:00.006338', '2025-11-20 02:25:08.377900', 20),
(22, '2025-12-07 01:36:00.000000', 2, '2025-11-20 02:25:08.382128', '2025-11-20 02:54:56.488654', 20),
(23, '2025-12-07 06:36:00.000000', 2, '2025-11-20 02:54:56.494574', '2025-11-20 02:59:51.000389', 20),
(24, '2025-12-07 11:36:00.000000', 2, '2025-11-20 02:59:51.005884', '2025-11-20 03:13:46.991273', 20),
(25, '2025-12-07 16:40:00.000000', 2, '2025-11-20 03:13:46.993709', '2025-11-20 07:38:21.727710', 20),
(26, '2025-11-25 21:00:00.000000', 1, '2025-11-23 02:57:22.088090', NULL, 24);

-- --------------------------------------------------------

--
-- Table structure for table `tasks_details`
--
-- Creation: Nov 16, 2025 at 01:33 AM
-- Last update: Nov 23, 2025 at 02:57 AM
--

CREATE TABLE `tasks_details` (
  `id` bigint NOT NULL,
  `details` longtext COLLATE utf8mb4_bin NOT NULL,
  `latest` smallint NOT NULL DEFAULT '1',
  `create_time` datetime(6) NOT NULL,
  `delete_time` datetime(6) DEFAULT NULL,
  `task_id` bigint NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

--
-- Dumping data for table `tasks_details`
--

INSERT INTO `tasks_details` (`id`, `details`, `latest`, `create_time`, `delete_time`, `task_id`) VALUES
(1, 'In MySQL, you can retrieve the nth row in a result set by using the LIMIT clause with an OFFSET. The syntax is LIMIT offset, row_count or LIMIT row_count OFFSET offset. \r\nUsing LIMIT and OFFSET\r\nTo get the nth row, you need to use an offset of n-1 because MySQL (and most SQL databases) uses zero-indexed offsets. \r\nsql\r\nSELECT * FROM your_table\r\nORDER BY column_to_order\r\nLIMIT 1 OFFSET (n - 1);\r\nAlternatively, using the comma syntax for LIMIT:\r\nsql\r\nSELECT * FROM your_table\r\nORDER BY column_to_order\r\nLIMIT (n - 1), 1;\r\nORDER BY column_to_order: This is essential. Without an ORDER BY clause, the order of rows is not guaranteed, and the \"nth\" row could change with each query execution.\r\nLIMIT 1: This specifies that you want to return only one row.\r\nOFFSET (n - 1): This tells MySQL to skip the first n-1 rows before starting to count the result set. \r\nExample: Retrieving the 5th row', 2, '2025-11-09 04:56:08.000000', '2025-11-20 07:37:59.928116', 1),
(2, 'Lorem ipsum indrigado. Navi sapto urdegan. Urague dorus beki heptim.', 1, '2025-11-17 10:17:33.562944', NULL, 12),
(3, 'Lorem ipsum indrigado. Navi sapto urdegan. Urague dorus beki heptim.', 1, '2025-11-17 10:30:05.237035', NULL, 13),
(4, 'Lorem ipsum indrigado. Navi sapto urdegan. Urague dorus beki heptim.', 1, '2025-11-17 10:35:29.746557', NULL, 14),
(5, 'MT record', 1, '2025-11-17 10:39:02.133142', NULL, 15),
(6, 'Updates\r\nLorem ipsum indrigado. Navi sapto urdegan. Urague dorus beki heptim.', 1, '2025-11-17 10:43:09.736793', NULL, 16),
(7, 'Updates\r\nLorem ipsum indrigado. Navi sapto urdegan. Urague dorus beki heptim.', 2, '2025-11-17 10:46:14.417226', '2025-11-20 07:48:22.471000', 17),
(8, 'Let\'s see if the wtahcer\'s table can be skipped now. We also added some error handling on the update operation.', 1, '2025-11-17 10:58:51.190337', NULL, 18),
(9, 'Updates\r\nLorem ipsum indrigado. Navi sapto urdegan. Urague dorus beki heptim.', 2, '2025-11-17 11:02:19.238408', '2025-11-20 03:21:29.615609', 19),
(10, 'Let\'s see what this round brings.', 2, '2025-11-17 11:08:01.089397', '2025-11-20 02:05:58.467874', 20),
(11, 'Let\'s see what this round brings.', 2, '2025-11-17 11:08:49.093977', '2025-11-19 12:51:21.323397', 21),
(12, 'This is simply a test! The test can go two ways. It can either be submitted. Or it cannot.', 1, '2025-11-17 11:09:45.214752', NULL, 22),
(13, 'I\'m CHANGING the details!!!!!!\r\n\r\n\r\nYey', 1, '2025-11-17 11:18:27.553438', NULL, 23),
(14, 'Let\'s see what this round brings.\r\n\r\ni will add this change!!!!', 2, '2025-11-17 12:18:34.427535', '2025-11-19 09:31:57.568329', 24),
(15, 'We hope this will go through.', 2, '2025-11-17 23:54:28.875372', '2025-11-18 09:56:11.514536', 25),
(16, 'Options\r\nTasks \r\nTickets \r\nClients\r\nSearch\r\n \r\n\r\nUpdates\r\nLorem ipsum indrigado. Navi sapto urdegan. Urague dorus beki heptim.', 1, '2025-11-19 09:00:13.367707', NULL, 25),
(17, 'UpdateView¶\nclass django.views.generic.edit.UpdateView¶\nA view that displays a form for editing an existing object, redisplaying the form with validation errors (if there are any) and saving changes to the object. This uses a form automatically generated from the object’s model class (unless a form class is manually specified).\n\nAncestors (MRO)\n\nThis view inherits methods and attributes from the following views:\n\ndjango.views.generic.detail.SingleObjectTemplateResponseMixin\n\ndjango.views.generic.base.TemplateResponseMixin\n\ndjango.views.generic.edit.BaseUpdateView\n\ndjango.views.generic.edit.ModelFormMixin\n\ndjango.views.generic.edit.FormMixin\n\ndjango.views.generic.detail.SingleObjectMixin\n\ndjango.views.generic.edit.ProcessFormView\n\ndjango.views.generic.base.View\n\nAttributes\n\ntemplate_name_suffix¶\nThe UpdateView page displayed to a GET request uses a template_name_suffix of \'_form\'. For example, changing this attribute to \'_update_form\' for a view updating objects for the example Author model would cause the default template_name to be \'myapp/author_update_form.html\'.\n\nobject¶\nWhen using UpdateView you have access to self.object, which is the object being updated.\n\nExample myapp/views.py:\n\nfrom django.views.generic.edit import UpdateView\nfrom myapp.models import Author\n\n\nclass AuthorUpdateView(UpdateView):\n    model = Author\n    fields = [\"name\"]\n    template_name_suffix = \"_update_form\"\nExample myapp/author_update_form.html:\n\n<form method=\"post\">{% csrf_token %}\n    {{ form.as_p }}\n    <input type=\"submit\" value=\"Update\">\n</form>\nclass django.views.generic.edit.BaseUpdateView¶\nA base view for updating an existing object instance. It is not intended to be used directly, but rather as a parent class of the django.views.generic.edit.UpdateView.\n\nAncestors (MRO)\n\nThis view inherits methods and attributes from the following views:\n\ndjango.views.generic.edit.ModelFormMixin\n\ndjango.views.generic.edit.ProcessFormView\n\nMethods\n\nget(request, *args, **kwargs)¶\nSets the current object instance (self.object).\n\npost(request, *args, **kwargs)¶\nSets the current object instance (self.object).\n\nDeleteView¶\nclass django.views.generic.edit.DeleteView¶\nA view that displays a confirmation page and deletes an existing object. The given object will only be deleted if the request method is POST. If this view is fetched via GET, it will display a confirmation page that should contain a form that POSTs to the same URL.\n\nAncestors (MRO)\n\nThis view inherits methods and attributes from the following views:\n\ndjango.views.generic.detail.SingleObjectTemplateResponseMixin\n\ndjango.views.generic.base.TemplateResponseMixin\n\ndjango.views.generic.edit.BaseDeleteView\n\ndjango.views.generic.edit.DeletionMixin\n\ndjango.views.generic.edit.FormMixin\n\ndjango.views.generic.base.ContextMixin\n\ndjango.views.generic.detail.BaseDetailView\n\ndjango.views.generic.detail.SingleObjectMixin\n\ndjango.views.generic.base.View\n\nAttributes\n\nform_class¶\nInherited from BaseDeleteView. The form class that will be used to confirm the request. By default django.forms.Form, resulting in an empty form that is always valid.\n\nBy providing your own Form subclass, you can add additional requirements, such as a confirmation checkbox, for example.\n\ntemplate_name_suffix¶\nThe DeleteView page displayed to a GET request uses a template_name_suffix of \'_confirm_delete\'. For example, changing this attribute to \'_check_delete\' for a view deleting objects for the example Author model would cause the default template_name to be \'myapp/author_check_delete.html\'.\n\nExample myapp/views.py:', 2, '2025-11-19 09:31:57.571886', '2025-11-19 12:44:26.799005', 24),
(18, 'UpdateView¶\r\nclass django.views.generic.edit.UpdateView¶\r\nA view that displays a form for editing an existing object, redisplaying the form with validation errors (if there are any) and saving changes to the object. This uses a form automatically generated from the object’s model class (unless a form class is manually specified).\r\n\r\nAncestors (MRO)\r\n\r\nThis view inherits methods and attributes from the following views:\r\n\r\ndjango.views.generic.detail.SingleObjectTemplateResponseMixin\r\n\r\ndjango.views.generic.base.TemplateResponseMixin\r\n\r\ndjango.views.generic.edit.BaseUpdateView\r\n\r\ndjango.views.generic.edit.ModelFormMixin\r\n\r\ndjango.views.generic.edit.FormMixin\r\n\r\ndjango.views.generic.detail.SingleObjectMixin\r\n\r\ndjango.views.generic.edit.ProcessFormView\r\n\r\ndjango.views.generic.base.View\r\n\r\nAttributes\r\n\r\ntemplate_name_suffix¶\r\nThe UpdateView page displayed to a GET request uses a template_name_suffix of \'_form\'. For example, changing this attribute to \'_update_form\' for a view updating objects for the example Author model would cause the default template_name to be \'myapp/author_update_form.html\'.\r\n\r\nobject¶\r\nWhen using UpdateView you have access to self.object, which is the object being updated.\r\n\r\nExample myapp/views.py:\r\n\r\nfrom django.views.generic.edit import UpdateView\r\nfrom myapp.models import Author\r\n\r\n\r\nclass AuthorUpdateView(UpdateView):\r\n    model = Author\r\n    fields = [\"name\"]\r\n    template_name_suffix = \"_update_form\"\r\nExample myapp/author_update_form.html:\r\n\r\n<form method=\"post\">{% csrf_token %}\r\n    {{ form.as_p }}\r\n    <input type=\"submit\" value=\"Update\">\r\n</form>\r\nclass django.views.generic.edit.BaseUpdateView¶\r\nA base view for updating an existing object instance. It is not intended to be used directly, but rather as a parent class of the django.views.generic.edit.UpdateView.\r\n\r\nAncestors (MRO)\r\n\r\nThis view inherits methods and attributes from the following views:\r\n\r\ndjango.views.generic.edit.ModelFormMixin\r\n\r\ndjango.views.generic.edit.ProcessFormView\r\n\r\nMethods\r\n\r\nget(request, *args, **kwargs)¶\r\nSets the current object instance (self.object).\r\n\r\npost(request, *args, **kwargs)¶\r\nSets the current object instance (self.object).\r\n\r\nDeleteView¶\r\nclass django.views.generic.edit.DeleteView¶\r\nA view that displays a confirmation page and deletes an existing object. The given object will only be deleted if the request method is POST. If this view is fetched via GET, it will display a confirmation page that should contain a form that POSTs to the same URL.\r\n\r\nAncestors (MRO)\r\n\r\nThis view inherits methods and attributes from the following views:\r\n\r\ndjango.views.generic.detail.SingleObjectTemplateResponseMixin\r\n\r\ndjango.views.generic.base.TemplateResponseMixin\r\n\r\ndjango.views.generic.edit.BaseDeleteView\r\n\r\ndjango.views.generic.edit.DeletionMixin\r\n\r\ndjango.views.generic.edit.FormMixin\r\n\r\ndjango.views.generic.base.ContextMixin\r\n\r\ndjango.views.generic.detail.BaseDetailView\r\n\r\ndjango.views.generic.detail.SingleObjectMixin\r\n\r\ndjango.views.generic.base.View\r\n\r\nAttributes\r\n\r\nform_class¶\r\nInherited from BaseDeleteView. The form class that will be used to confirm the request. By default django.forms.Form, resulting in an empty form that is always valid.\r\n\r\nBy providing your own Form subclass, you can add additional requirements, such as a confirmation checkbox, for example.\r\n\r\ntemplate_name_suffix¶\r\nThe DeleteView page displayed to a GET request uses a template_name_suffix of \'_confirm_delete\'. For example, changing this attribute to \'_check_delete\' for a view deleting objects for the example Author model would cause the default template_name to be \'myapp/author_check_delete.html\'.\r\n\r\nExample myapp/views.py:', 2, '2025-11-19 12:44:26.802256', '2025-11-23 02:57:22.079437', 24),
(19, 'A variable is a segment of memory with a unique name used to hold data that will later be processed. Although each programming language has a different mechanism for declaring variables, the name and the data that will be assigned to each variable are always the same. They are capable of storing values of data types.\r\n\r\nThe assignment operator(=) assigns the value provided to its right to the variable name given to its left. Given is the basic syntax of variable declaration:\r\n\r\nAssign Values to Multiple Variables in One Line\r\nGiven above is the mechanism for assigning just variables in Python but it is possible to assign multiple variables at the same time. Python assigns values from right to left. When assigning multiple variables in a single line, different variable names are provided to the left of the assignment operator separated by a comma. The same goes for their respective values except they should be to the right of the assignment operator.\r\n\r\nWhile declaring variables in this fashion one must be careful with the order of the names and their corresponding value first variable name to the left of the assignment operator is assigned with the first value to its right and so on.', 1, '2025-11-19 12:51:21.326136', NULL, 21),
(20, 'Handle Naive Datetimes (If Necessary)\r\nIf you have a \"naive\" (timezone-unaware) datetime object created elsewhere in your code, you cannot compare it directly with an aware one; it will raise an exception. You must make the naive object aware using the timezone.make_aware() helper function, which applies the current time zone defined in your settings', 2, '2025-11-20 02:05:58.470261', '2025-11-20 07:38:21.693466', 20),
(21, 'Updates\r\nLorem ipsum indrigado. Navi sapto urdegan. Urague dorus beki heptim.\r\n\r\nKey Components\r\nredirect(): This function returns an HttpResponseRedirect to the appropriate URL.\r\nreverse(): This utility is often used within redirect() to look up the URL by its symbolic name defined in your urls.py file. This makes your code more maintainable because you only change the actual URL path in one place. \r\nExample in urls.py', 2, '2025-11-20 03:21:29.620223', '2025-11-20 07:10:51.525504', 19),
(22, 'We shall attempt to summarize the ways thi ticket should be seen after the update:\r\n\r\n1) The title should be changed to having #1 prefixed to it.\r\n\r\n2) The status has changed from \'started\' => \'queued\'\r\n\r\n3) The description has changed this writeup.\r\n\r\n4) The deadline will be 4pm on Nov 29, 2025', 1, '2025-11-23 02:57:22.082584', NULL, 24);

-- --------------------------------------------------------

--
-- Table structure for table `tasks_status`
--
-- Creation: Nov 16, 2025 at 01:33 AM
-- Last update: Nov 23, 2025 at 02:57 AM
--

CREATE TABLE `tasks_status` (
  `id` bigint NOT NULL,
  `status` varchar(20) COLLATE utf8mb4_bin NOT NULL,
  `latest` smallint NOT NULL DEFAULT '1',
  `create_time` datetime(6) NOT NULL,
  `delete_time` datetime(6) DEFAULT NULL,
  `task_id` bigint NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

--
-- Dumping data for table `tasks_status`
--

INSERT INTO `tasks_status` (`id`, `status`, `latest`, `create_time`, `delete_time`, `task_id`) VALUES
(1, 'queued', 2, '2025-11-09 04:57:36.000000', '2025-11-20 07:37:59.966266', 1),
(2, 'queued', 1, '2025-11-17 10:17:33.566193', NULL, 12),
(3, 'queued', 1, '2025-11-17 10:30:05.240261', NULL, 13),
(4, 'queued', 1, '2025-11-17 10:35:29.750322', NULL, 14),
(5, 'queued', 1, '2025-11-17 10:39:02.136629', NULL, 15),
(6, 'queued', 1, '2025-11-17 10:43:09.739808', NULL, 16),
(7, 'queued', 2, '2025-11-17 10:46:14.420523', '2025-11-20 07:48:22.502046', 17),
(8, 'queued', 1, '2025-11-17 10:58:51.194639', NULL, 18),
(9, 'queued', 2, '2025-11-17 11:02:19.241862', '2025-11-20 03:21:29.627155', 19),
(10, 'queued', 2, '2025-11-17 11:08:01.092234', '2025-11-20 02:05:58.478752', 20),
(11, 'queued', 1, '2025-11-17 11:08:49.103842', NULL, 21),
(12, 'queued', 1, '2025-11-17 11:09:45.218804', NULL, 22),
(13, 'queued', 1, '2025-11-17 11:18:27.558753', NULL, 23),
(14, 'started', 2, '2025-11-17 12:18:34.430927', '2025-11-19 09:31:57.580310', 24),
(15, 'queued', 2, '2025-11-17 23:54:28.880287', '2025-11-19 09:00:13.377142', 25),
(16, 'queued', 1, '2025-11-19 09:00:13.379418', NULL, 25),
(17, 'started', 2, '2025-11-19 09:31:57.583058', '2025-11-23 02:57:22.090646', 24),
(18, 'started', 2, '2025-11-20 02:05:58.481480', '2025-11-20 07:38:21.731724', 20),
(19, 'awaitingfeedback', 2, '2025-11-20 03:21:29.631494', '2025-11-20 03:27:27.445206', 19),
(20, 'reassigned', 2, '2025-11-20 03:27:27.447773', '2025-11-20 07:10:51.557977', 19),
(21, 'queued', 1, '2025-11-23 02:57:22.093267', NULL, 24);

-- --------------------------------------------------------

--
-- Table structure for table `tasks_task`
--
-- Creation: Nov 09, 2025 at 09:54 AM
-- Last update: Nov 23, 2025 at 02:57 AM
--

CREATE TABLE `tasks_task` (
  `id` bigint NOT NULL,
  `description` varchar(255) COLLATE utf8mb4_bin NOT NULL,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `delete_time` datetime(6) DEFAULT NULL,
  `creator_id` int NOT NULL,
  `parent_id` bigint DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

--
-- Dumping data for table `tasks_task`
--

INSERT INTO `tasks_task` (`id`, `description`, `create_time`, `update_time`, `delete_time`, `creator_id`, `parent_id`) VALUES
(1, 'This is a test task. To see if this opeation is working.', '2025-11-04 09:11:16.000000', '2025-11-20 07:37:59.981241', '2025-11-20 07:37:59.981241', 1, NULL),
(12, 'My second ticket!', '2025-11-17 10:17:33.560877', '2025-11-17 10:17:33.560877', NULL, 1, NULL),
(13, 'My second ticket!', '2025-11-17 10:30:05.234536', '2025-11-17 10:30:05.234536', NULL, 1, NULL),
(14, 'My second ticket!', '2025-11-17 10:35:29.744008', '2025-11-17 10:35:29.744008', NULL, 1, NULL),
(15, 'My second ticket!', '2025-11-17 10:39:02.126202', '2025-11-17 10:39:02.126202', NULL, 1, NULL),
(16, 'My second ticket!', '2025-11-17 10:43:09.734548', '2025-11-17 10:43:09.734548', NULL, 1, NULL),
(17, 'My second ticket!', '2025-11-17 10:46:14.415280', '2025-11-20 07:48:22.508966', '2025-11-20 07:48:22.508966', 1, NULL),
(18, 'Third ticket Tasks Management Console', '2025-11-17 10:58:51.188163', '2025-11-17 10:58:51.188163', NULL, 1, NULL),
(19, 'Nineteenth Task', '2025-11-17 11:02:19.236351', '2025-11-20 07:36:16.413843', '2025-11-20 07:36:16.413843', 1, 1),
(20, 'Twentieth Ticket!', '2025-11-17 11:08:01.087089', '2025-11-20 07:38:21.745733', '2025-11-20 07:38:21.745733', 1, 1),
(21, 'Let\'s see how this edit goes.', '2025-11-17 11:08:49.091865', '2025-11-19 12:51:21.320247', NULL, 1, NULL),
(22, 'Yey! Ticket inserts are working!', '2025-11-17 11:09:45.211670', '2025-11-17 11:09:45.211670', NULL, 1, NULL),
(23, 'Yey! Ticket inserts are working!', '2025-11-17 11:18:27.549386', '2025-11-17 11:18:27.549386', NULL, 1, NULL),
(24, '#1 This will be a complete edit', '2025-11-17 12:18:34.424176', '2025-11-23 02:57:22.068565', NULL, 1, NULL),
(25, 'Now We Enter a DESCRIPTION', '2025-11-17 23:54:28.866352', '2025-11-19 09:00:13.364306', NULL, 1, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `tasks_visibility`
--
-- Creation: Nov 16, 2025 at 01:33 AM
-- Last update: Nov 20, 2025 at 07:48 AM
--

CREATE TABLE `tasks_visibility` (
  `id` bigint NOT NULL,
  `visibility` varchar(20) COLLATE utf8mb4_bin NOT NULL,
  `latest` smallint NOT NULL DEFAULT '1',
  `create_time` datetime(6) NOT NULL,
  `delete_time` datetime(6) DEFAULT NULL,
  `task_id` bigint NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

--
-- Dumping data for table `tasks_visibility`
--

INSERT INTO `tasks_visibility` (`id`, `visibility`, `latest`, `create_time`, `delete_time`, `task_id`) VALUES
(1, 'private', 2, '2025-11-09 04:58:34.000000', '2025-11-20 07:37:59.969824', 1),
(2, 'private', 1, '2025-11-17 10:17:33.567695', NULL, 12),
(3, 'private', 1, '2025-11-17 10:30:05.241991', NULL, 13),
(4, 'private', 1, '2025-11-17 10:35:29.751688', NULL, 14),
(5, 'private', 1, '2025-11-17 10:39:02.138092', NULL, 15),
(6, 'private', 1, '2025-11-17 10:43:09.741364', NULL, 16),
(7, 'private', 2, '2025-11-17 10:46:14.421816', '2025-11-20 07:48:22.503789', 17),
(8, 'private', 1, '2025-11-17 10:58:51.198157', NULL, 18),
(9, 'private', 2, '2025-11-17 11:02:19.243205', '2025-11-20 03:21:29.635840', 19),
(10, 'private', 2, '2025-11-17 11:08:01.093631', '2025-11-20 02:05:58.484373', 20),
(11, 'private', 1, '2025-11-17 11:08:49.106181', NULL, 21),
(12, 'private', 1, '2025-11-17 11:09:45.220196', NULL, 22),
(13, 'private', 1, '2025-11-17 11:18:27.562665', NULL, 23),
(14, 'private', 2, '2025-11-17 12:18:34.432181', '2025-11-19 09:31:57.586181', 24),
(15, 'private', 2, '2025-11-17 23:54:28.882671', '2025-11-19 09:00:13.381637', 25),
(16, 'private', 1, '2025-11-19 09:00:13.383744', NULL, 25),
(17, 'internal', 2, '2025-11-19 09:31:57.588780', '2025-11-19 12:44:26.811634', 24),
(18, 'private', 1, '2025-11-19 12:44:26.814470', NULL, 24),
(19, 'viewed', 2, '2025-11-20 02:05:58.487707', '2025-11-20 03:16:07.965433', 20),
(20, 'reassigned', 2, '2025-11-20 03:16:07.968836', '2025-11-20 07:38:21.735663', 20),
(21, 'organization', 2, '2025-11-20 03:21:29.640895', '2025-11-20 03:22:15.266668', 19),
(22, 'private', 2, '2025-11-20 03:22:15.271950', '2025-11-20 07:10:51.559164', 19);

-- --------------------------------------------------------

--
-- Table structure for table `tasks_watcher`
--
-- Creation: Nov 16, 2025 at 01:33 AM
--

CREATE TABLE `tasks_watcher` (
  `id` bigint NOT NULL,
  `latest` smallint NOT NULL DEFAULT '1',
  `create_time` datetime(6) NOT NULL,
  `delete_time` datetime(6) DEFAULT NULL,
  `task_id` bigint NOT NULL,
  `watcher_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Indexes for table `auth_user`
--
ALTER TABLE `auth_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indexes for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  ADD KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`);

--
-- Indexes for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  ADD KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`);

--
-- Indexes for table `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Indexes for table `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- Indexes for table `tasks_assignment`
--
ALTER TABLE `tasks_assignment`
  ADD PRIMARY KEY (`id`),
  ADD KEY `tasks_assignment_assignee_id_9a363d7c_fk_auth_user_id` (`assignee_id`),
  ADD KEY `tasks_assignment_assignor_id_a74cf74e_fk_auth_user_id` (`assignor_id`),
  ADD KEY `tasks_assignment_task_id_53c45b5e_fk_tasks_task_id` (`task_id`);

--
-- Indexes for table `tasks_deadline`
--
ALTER TABLE `tasks_deadline`
  ADD PRIMARY KEY (`id`),
  ADD KEY `tasks_deadline_task_id_90840f11_fk_tasks_task_id` (`task_id`);

--
-- Indexes for table `tasks_details`
--
ALTER TABLE `tasks_details`
  ADD PRIMARY KEY (`id`),
  ADD KEY `tasks_details_task_id_83da28db_fk_tasks_task_id` (`task_id`);

--
-- Indexes for table `tasks_status`
--
ALTER TABLE `tasks_status`
  ADD PRIMARY KEY (`id`),
  ADD KEY `tasks_status_task_id_637fc821_fk_tasks_task_id` (`task_id`);

--
-- Indexes for table `tasks_task`
--
ALTER TABLE `tasks_task`
  ADD PRIMARY KEY (`id`),
  ADD KEY `tasks_task_creator_id_ca3b6762_fk_auth_user_id` (`creator_id`),
  ADD KEY `tasks_task_parent_id_ee6a2001_fk_tasks_task_id` (`parent_id`);

--
-- Indexes for table `tasks_visibility`
--
ALTER TABLE `tasks_visibility`
  ADD PRIMARY KEY (`id`),
  ADD KEY `tasks_visibility_task_id_a8b84032_fk_tasks_task_id` (`task_id`);

--
-- Indexes for table `tasks_watcher`
--
ALTER TABLE `tasks_watcher`
  ADD PRIMARY KEY (`id`),
  ADD KEY `tasks_watcher_task_id_8cf84614_fk_tasks_task_id` (`task_id`),
  ADD KEY `tasks_watcher_watcher_id_3e904427_fk_auth_user_id` (`watcher_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=73;

--
-- AUTO_INCREMENT for table `auth_user`
--
ALTER TABLE `auth_user`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;

--
-- AUTO_INCREMENT for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- AUTO_INCREMENT for table `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=27;

--
-- AUTO_INCREMENT for table `tasks_assignment`
--
ALTER TABLE `tasks_assignment`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `tasks_deadline`
--
ALTER TABLE `tasks_deadline`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=27;

--
-- AUTO_INCREMENT for table `tasks_details`
--
ALTER TABLE `tasks_details`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;

--
-- AUTO_INCREMENT for table `tasks_status`
--
ALTER TABLE `tasks_status`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- AUTO_INCREMENT for table `tasks_task`
--
ALTER TABLE `tasks_task`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;

--
-- AUTO_INCREMENT for table `tasks_visibility`
--
ALTER TABLE `tasks_visibility`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;

--
-- AUTO_INCREMENT for table `tasks_watcher`
--
ALTER TABLE `tasks_watcher`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Constraints for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Constraints for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `tasks_assignment`
--
ALTER TABLE `tasks_assignment`
  ADD CONSTRAINT `tasks_assignment_assignee_id_9a363d7c_fk_auth_user_id` FOREIGN KEY (`assignee_id`) REFERENCES `auth_user` (`id`),
  ADD CONSTRAINT `tasks_assignment_assignor_id_a74cf74e_fk_auth_user_id` FOREIGN KEY (`assignor_id`) REFERENCES `auth_user` (`id`),
  ADD CONSTRAINT `tasks_assignment_task_id_53c45b5e_fk_tasks_task_id` FOREIGN KEY (`task_id`) REFERENCES `tasks_task` (`id`);

--
-- Constraints for table `tasks_deadline`
--
ALTER TABLE `tasks_deadline`
  ADD CONSTRAINT `tasks_deadline_task_id_90840f11_fk_tasks_task_id` FOREIGN KEY (`task_id`) REFERENCES `tasks_task` (`id`);

--
-- Constraints for table `tasks_details`
--
ALTER TABLE `tasks_details`
  ADD CONSTRAINT `tasks_details_task_id_83da28db_fk_tasks_task_id` FOREIGN KEY (`task_id`) REFERENCES `tasks_task` (`id`);

--
-- Constraints for table `tasks_status`
--
ALTER TABLE `tasks_status`
  ADD CONSTRAINT `tasks_status_task_id_637fc821_fk_tasks_task_id` FOREIGN KEY (`task_id`) REFERENCES `tasks_task` (`id`);

--
-- Constraints for table `tasks_task`
--
ALTER TABLE `tasks_task`
  ADD CONSTRAINT `tasks_task_creator_id_ca3b6762_fk_auth_user_id` FOREIGN KEY (`creator_id`) REFERENCES `auth_user` (`id`),
  ADD CONSTRAINT `tasks_task_parent_id_ee6a2001_fk_tasks_task_id` FOREIGN KEY (`parent_id`) REFERENCES `tasks_task` (`id`);

--
-- Constraints for table `tasks_visibility`
--
ALTER TABLE `tasks_visibility`
  ADD CONSTRAINT `tasks_visibility_task_id_a8b84032_fk_tasks_task_id` FOREIGN KEY (`task_id`) REFERENCES `tasks_task` (`id`);

--
-- Constraints for table `tasks_watcher`
--
ALTER TABLE `tasks_watcher`
  ADD CONSTRAINT `tasks_watcher_task_id_8cf84614_fk_tasks_task_id` FOREIGN KEY (`task_id`) REFERENCES `tasks_task` (`id`),
  ADD CONSTRAINT `tasks_watcher_watcher_id_3e904427_fk_auth_user_id` FOREIGN KEY (`watcher_id`) REFERENCES `auth_user` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
