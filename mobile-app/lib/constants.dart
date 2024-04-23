import 'package:flutter/material.dart';

const String cmpAPIUrl = 'http://localhost:8000/api/';


const primaryColor = Color(0xFF4A794C);
const secondaryColor = Color(0xFFE0E0E0);
const backgroundColor = Color(0xFFF5F5F5);
const textColor = Color(0x1F444444);
const textColorLight = Color(0xFF747474);
const textColorDark = Color(0xFF101010);
const iconColor = Color(0xFF6C63FF);
const iconColorLight = Color(0xFFE0E0E0);
const iconColorDark = Color(0xFF101010);
const errorColor = Color(0xFFD32F2F);
const successColor = Color(0xFF388E3C);


class AppVersionUtil {
  static const String appVersion = '1.0.0';
  static String buildNumber = '1';
  static String appName = 'Comrade Marketplace';
  static String packageName = 'com.comrade.marketplace';

  static String getAppVersion() {
    return appVersion;
  
  }

  static String getBuildNumber() {
    return buildNumber;
  }

  static String getAppName() {
    return appName;
  }

  static String getPackageName() {
    return packageName;
  }
}

void successSnackBar(BuildContext context, String message,
    {Duration duration = const Duration(seconds: 5)}) {
  ScaffoldMessenger.of(context).showSnackBar(
    SnackBar(
      content: Text(message),
      backgroundColor: Colors.green,
      duration: duration,
    ),
  );
}

void errorSnackBar(BuildContext context, String message,
    {Duration duration = const Duration(seconds: 8)}) {
  ScaffoldMessenger.of(context).showSnackBar(
    SnackBar(
      content: Text(message),
      backgroundColor: Colors.red,
      duration: duration,
    ),
  );
}
