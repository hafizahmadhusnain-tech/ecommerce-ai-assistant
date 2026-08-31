import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { authService } from '../services/api';

export default function Login() {
  const [username, setUsername] = useState('testuser');
  const [password, setPassword] = useState('password123');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    if (e) e.preventDefault();
    setError('');
    setLoading(true);
    try {
      const data = await authService.login(username, password);
      localStorage.setItem('token', data.access_token);
      navigate('/chat');
    } catch (err) {
      setError('Invalid credentials. Try testuser / password123');
    } finally {
      setLoading(false);
    }
  };

  const handleQuickLogin = async () => {
    setUsername('testuser');
    setPassword('password123');
    setLoading(true);
    setError('');
    try {
      const data = await authService.login('testuser', 'password123');
      localStorage.setItem('token', data.access_token);
      navigate('/chat');
    } catch (err) {
      setError('Connection issue with backend server.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-950 px-4 relative overflow-hidden">
      {/* Ambient background glow */}
      <div className="absolute top-1/4 left-1/2 -translate-x-1/2 w-96 h-96 bg-indigo-600/20 rounded-full blur-3xl pointer-events-none"></div>
      <div className="absolute bottom-1/4 left-1/3 w-80 h-80 bg-purple-600/15 rounded-full blur-3xl pointer-events-none"></div>

      <div className="bg-slate-900/80 backdrop-blur-2xl border border-slate-800/80 p-8 rounded-3xl shadow-2xl w-full max-w-md relative z-10">
        {/* Header with Glowing Mini Orb */}
        <div className="flex flex-col items-center mb-8">
          <div className="w-16 h-16 rounded-full bg-gradient-to-tr from-indigo-500 via-purple-500 to-cyan-400 p-[2px] shadow-lg shadow-indigo-500/30 mb-4 animate-pulse">
            <div className="w-full h-full bg-slate-950 rounded-full flex items-center justify-center text-2xl">
              ✨
            </div>
          </div>
          <h2 className="text-2xl font-bold text-white tracking-tight">Nova Store AI</h2>
          <p className="text-slate-400 text-xs mt-1">Next-Gen Intelligent Shopping Assistant</p>
        </div>
        
        {error && (
          <div className="bg-red-500/10 border border-red-500/30 text-red-400 text-xs p-3 rounded-xl mb-5 text-center">
            {error}
          </div>
        )}
        
        <form onSubmit={handleLogin} className="space-y-4">
          <div>
            <label className="block text-slate-300 text-xs font-semibold uppercase tracking-wider mb-2">Username</label>
            <input 
              type="text" 
              value={username} 
              onChange={(e) => setUsername(e.target.value)} 
              className="w-full bg-slate-950/80 border border-slate-800 rounded-xl px-4 py-3 text-sm text-white focus:outline-none focus:border-indigo-500 transition-all placeholder-slate-600" 
              placeholder="e.g. testuser" 
              required 
            />
          </div>
          <div>
            <label className="block text-slate-300 text-xs font-semibold uppercase tracking-wider mb-2">Password</label>
            <input 
              type="password" 
              value={password} 
              onChange={(e) => setPassword(e.target.value)} 
              className="w-full bg-slate-950/80 border border-slate-800 rounded-xl px-4 py-3 text-sm text-white focus:outline-none focus:border-indigo-500 transition-all placeholder-slate-600" 
              placeholder="••••••••" 
              required 
            />
          </div>
          
          <button 
            type="submit" 
            disabled={loading} 
            className="w-full bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white font-medium py-3 rounded-xl transition-all shadow-lg shadow-indigo-600/25 active:scale-[0.99] disabled:opacity-50 text-sm cursor-pointer"
          >
            {loading ? 'Signing in...' : 'Sign In to Assistant'}
          </button>
        </form>

        <div className="relative my-6 text-center">
          <div className="absolute inset-0 flex items-center"><div className="w-full border-t border-slate-800"></div></div>
          <span className="relative bg-slate-900 px-3 text-xs text-slate-500 uppercase tracking-widest font-semibold">Demo Access</span>
        </div>

        <button 
          onClick={handleQuickLogin}
          disabled={loading}
          type="button"
          className="w-full bg-slate-800/80 hover:bg-slate-700/80 text-slate-200 border border-slate-700/60 font-medium py-2.5 rounded-xl transition-all text-xs flex items-center justify-center gap-2 cursor-pointer"
        >
          <span>⚡</span>
          <span>1-Click Instant Demo Login</span>
        </button>
      </div>
    </div>
  );
}