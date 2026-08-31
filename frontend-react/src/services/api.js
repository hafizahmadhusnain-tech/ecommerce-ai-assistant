import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8000/api/v1';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
});

// Request interceptor to auto-inject JWT Token
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
}, (error) => {
  return Promise.reject(error);
});

export const authService = {
  login: async (username, password) => {
    // FastAPI standard OAuth2 form data expects URLSearchParams
    const formData = new URLSearchParams();
    formData.append('username', username);
    formData.append('password', password);
    
    const response = await apiClient.post('/auth/login', formData, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    });
    return response.data;
  }
};

export const chatService = {
  sendMessage: async (message) => {
    const response = await apiClient.post('/chat', { message, user_id: "dynamic" });
    return response.data;
  },

  streamMessage: async (message, { onToken, onComplete, onError, signal } = {}) => {
    const token = localStorage.getItem('token');
    let hasCompleted = false;

    const triggerComplete = (fullResp) => {
      if (!hasCompleted) {
        hasCompleted = true;
        onComplete?.(fullResp);
      }
    };

    try {
      const response = await fetch(`${API_BASE_URL}/chat/stream`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...(token ? { 'Authorization': `Bearer ${token}` } : {})
        },
        body: JSON.stringify({ message, user_id: "dynamic" }),
        signal
      });

      if (!response.ok) {
        throw new Error(`Server status ${response.status}`);
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let buffer = '';

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n');
        buffer = lines.pop() || '';

        for (const line of lines) {
          const trimmed = line.trim();
          if (trimmed.startsWith('data: ')) {
            const jsonStr = trimmed.slice(6);
            try {
              const data = JSON.parse(jsonStr);
              if (data.token) {
                onToken?.(data.token);
              }
              if (data.done) {
                triggerComplete(data.full_response);
              }
              if (data.error) {
                onError?.(new Error(data.error));
              }
            } catch (e) {
              // Ignore partial parsing errors
            }
          }
        }
      }
      triggerComplete();
    } catch (err) {
      if (err.name !== 'AbortError') {
        onError?.(err);
      }
    }
  }
};

export default apiClient;