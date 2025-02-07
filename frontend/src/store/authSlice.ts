import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface AuthState {
  token: string | null;
  userEmail: string | null;
}

const initialState: AuthState = {
  token: null,
  userEmail: null,
};

const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    setCredentials: (state, action: PayloadAction<{ token: string; email: string }>) => {
      state.token = action.payload.token;
      state.userEmail = action.payload.email;
    },
    clearCredentials: (state) => {
      state.token = null;
      state.userEmail = null;
    },
  },
});

export const { setCredentials, clearCredentials } = authSlice.actions;
export default authSlice.reducer;
