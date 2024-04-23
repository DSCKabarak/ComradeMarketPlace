import 'package:flutter/material.dart';
import 'package:internet_connection_checker_plus/internet_connection_checker_plus.dart';

class ConnectivityProvider with ChangeNotifier {
  bool _isOnline = true;
  Future<bool> checkInternetConnection() async {
    bool connectivityCheck = await InternetConnection().hasInternetAccess;

    if (connectivityCheck != _isOnline) {
      _isOnline = connectivityCheck;
      notifyListeners();
    }
    return _isOnline;
  }

  bool get isOnline => _isOnline;
}
