class UserModel {
  final String email;
  final String accessToken;
  final String refreshToken;

  UserModel({
    required this.email,
    required this.accessToken,
    required this.refreshToken,
  });

  Map<String, dynamic> toMap() {
    return {
      'email': email,
      'accessToken': accessToken,
      'refreshToken': refreshToken,
    };
  }

  factory UserModel.fromMap(Map<String, dynamic> map) {
    return UserModel(
      email: map['email'],
      accessToken: map['accessToken'],
      refreshToken: map['refreshToken'],
    );
  }

  UserModel copyWith({
    String? email,
    String? accessToken,
    String? refreshToken,
  }) {
    return UserModel(
      email: email ?? this.email,
      accessToken: accessToken ?? this.accessToken,
      refreshToken: refreshToken ?? this.refreshToken,
    );
  }
}

