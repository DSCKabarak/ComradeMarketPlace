import React from 'react'
import { Navigate } from 'react-router-dom'

function PrivateRoute({ isAuthenticated, children }) {
  if (!isAuthenticated) {
    return <Navigate to="/" replace />
  }
  return children
}

export default PrivateRoute