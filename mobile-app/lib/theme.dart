import 'package:flutter/material.dart';
import 'package:cmp/constants.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';


ThemeData appTheme(BuildContext context) {
  // Initialize ScreenUtil
  ScreenUtil.init(
    context,
    designSize: const Size(375, 812),
    minTextAdapt: true,
  );

  return ThemeData(
    primaryColor: primaryColor,
    hintColor: secondaryColor,
    scaffoldBackgroundColor: backgroundColor,
    textTheme: TextTheme(
      displayLarge: TextStyle(
        fontSize: 24.sp,
        color: textColor,
        fontWeight: FontWeight.bold,
      ),
      displayMedium: TextStyle(
        fontSize: 18.sp,
        color: textColor,
        fontWeight: FontWeight.bold,
      ),
      displaySmall: TextStyle(
        fontSize: 14.sp,
        color: textColor,
        fontWeight: FontWeight.bold,
      ),
    ),
    appBarTheme: AppBarTheme(
      backgroundColor: primaryColor,
      titleTextStyle: TextStyle(
        fontSize: 18.sp,
        color: textColor,
        fontWeight: FontWeight.bold,
      ),
    ),
    iconTheme: const IconThemeData(
      color: iconColor,
    ),
    colorScheme: ColorScheme.fromSwatch(
      primarySwatch: MaterialColor(
        primaryColor.value,
        const <int, Color>{
          50: primaryColor,
          100: primaryColor,
          200: primaryColor,
          300: primaryColor,
          400: primaryColor,
          500: primaryColor,
          600: primaryColor,
          700: primaryColor,
          800: primaryColor,
          900: primaryColor,
        },
      ),
      backgroundColor: backgroundColor,
      cardColor: secondaryColor,
    ).copyWith(
      background: backgroundColor,
    ),
  );
}