#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <memory>
#include <map>
#include <ctime>
#include <iomanip>

class LogFileManager {
private:
    std::map<std::string, std::unique_ptr<std::ofstream>> files;

    std::string getCurrentTime() {
        std::time_t now = std::time(nullptr);
        std::tm* ltm = std::localtime(&now);
        char buffer[80];
        std::strftime(buffer, sizeof(buffer), "[%Y-%m-%d %H:%M:%S] ", ltm);
        return std::string(buffer);
    }

public:
    void openLogFile(const std::string& filename) {
        if (files.find(filename) == files.end()) {
            auto file = std::make_unique<std::ofstream>(filename, std::ios::app);
            if (!file->is_open()) return;
            files[filename] = std::move(file);
        }
    }

    void writeLog(const std::string& filename, const std::string& message) {
        if (files.find(filename) != files.end()) {
            *files[filename] << getCurrentTime() << message << std::endl;
        }
    }

    std::vector<std::string> readLogs(const std::string& filename) {
        std::vector<std::string> logs;
        std::ifstream file(filename);
        std::string line;
        if (file.is_open()) {
            while (std::getline(file, line)) {
                logs.push_back(line);
            }
            file.close();
        }
        return logs;
    }

    void closeLogFile(const std::string& filename) {
        auto it = files.find(filename);
        if (it != files.end()) {
            it->second->close();
            files.erase(it);
        }
    }

    LogFileManager() = default;
    LogFileManager(const LogFileManager&) = delete;
    LogFileManager& operator=(const LogFileManager&) = delete;
};

int main() {
    LogFileManager manager;

    manager.openLogFile("error.log");
    manager.openLogFile("debug.log");
    manager.openLogFile("info.log");

    manager.writeLog("error.log", "Database connection failed");
    manager.writeLog("debug.log", "User login attempt");
    manager.writeLog("info.log", "Server started successfully");

    std::vector<std::string> errorLogs = manager.readLogs("error.log");

    std::cout << "// error.log 파일 내용" << std::endl;
    if (!errorLogs.empty()) std::cout << errorLogs.back() << std::endl << std::endl;

    std::cout << "// debug.log 파일 내용" << std::endl;
    std::vector<std::string> debugLogs = manager.readLogs("debug.log");
    if (!debugLogs.empty()) std::cout << debugLogs.back() << std::endl << std::endl;

    std::cout << "// info.log 파일 내용" << std::endl;
    std::vector<std::string> infoLogs = manager.readLogs("info.log");
    if (!infoLogs.empty()) std::cout << infoLogs.back() << std::endl << std::endl;

    std::cout << "// readLogs 반환값" << std::endl;
    if (!errorLogs.empty()) {
        std::cout << "errorLogs[0] = \"" << errorLogs.back() << "\"" << std::endl;
    }

    return 0;
}
