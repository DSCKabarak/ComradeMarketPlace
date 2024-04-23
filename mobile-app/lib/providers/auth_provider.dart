import 'dart:convert';
import 'package:cmp/models/user_model.dart';
import 'package:http/http.dart' as http;
import 'package:flutter/material.dart';
import 'package:cmp/constants.dart';
import 'package:cmp/providers/connection_provider.dart';
import 'package:cmp/providers/http_response_handler.dart';
import 'package:shared_preferences/shared_preferences.dart';

class AuthProvider with ChangeNotifier {
  UserModel _user = UserModel(
    email: '',
    accessToken: '',
    refreshToken: '',
  );

  UserModel? get user => _user;

  setAccessToken(String accessToken) {
    if (user != null) {
      _user = _user.copyWith(accessToken: accessToken);
    }
    notifyListeners();
  }

  void setUser(UserModel userModel) {
    _user = userModel;
    notifyListeners();
  }

  void clearUser() {
    _user = UserModel(
      email: '',
      accessToken: '',
      refreshToken: '',
    );
    notifyListeners();
  }

  Future<void> login({
    required BuildContext context,
    required String email,
    required String password,
  }) async {
    final prefs = await SharedPreferences.getInstance();

    final AuthProvider authProvider = AuthProvider();

    final http.Response repsonse = await http.post(
      Uri.parse(
        '${cmpAPIUrl}api/accounts/login/',
      ),
      body: {
        'email': email,
        'password': password,
      },
    );
  }
}
