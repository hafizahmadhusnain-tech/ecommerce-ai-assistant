import React, { useState, useEffect, useRef, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { chatService } from '../services/api';

// Suggestion quick prompts
const QUICK_PROMPTS = [
  { label: '🎧 Wireless Earbuds', query: 'Show me wireless earbuds in stock' },
  { label: '👟 Running Shoes', query: 'Do you have AeroStride Running Shoes?' },
  { label: '🛒 Store Categories', query: 'What categories and products do you sell?' },
];

export default function Chat() {
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: '👋 Hello! I am **Nova**, your intelligent e-commerce shopping assistant. Ask me anything about our products, check live in-stock availability, or track your orders.'
    }
  ]);
  const [input, setInput] = useState('');
  const [orbState, setOrbState] = useState('idle'); // 'idle' | 'listening' | 'thinking' | 'speaking'
  const [isListening, setIsListening] = useState(false);
  const [voiceOutputEnabled, setVoiceOutputEnabled] = useState(false);
  const [streamingText, setStreamingText] = useState('');
  const [transcript, setTranscript] = useState('');

  const [voiceStatus, setVoiceStatus] = useState('');

  const messagesEndRef = useRef(null);
  const recognitionRef = useRef(null);
  const latestSpeechRef = useRef('');
  const handleSendMessageRef = useRef();
  const navigate = useNavigate();

  // Scroll to bottom
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, streamingText, orbState]);

  // Send message with streaming (forward definition for recognition.onend)
  const handleSendMessage = async (textToSend) => {
    const query = (textToSend || input).trim();
    if (!query || orbState === 'thinking' || orbState === 'speaking') return;

    if (isListening && recognitionRef.current) {
      latestSpeechRef.current = '';
      try {
        recognitionRef.current.stop();
      } catch (e) {}
      setIsListening(false);
    }

    // Add user message
    const userMsg = { role: 'user', content: query };
    setMessages((prev) => [...prev, userMsg]);
    setInput('');
    setTranscript('');
    setVoiceStatus('');
    setOrbState('thinking');
    setStreamingText('');

    let accumulated = '';
    let isFinished = false;

    await chatService.streamMessage(query, {
      onToken: (token) => {
        setOrbState('speaking');
        accumulated += token;
        setStreamingText(accumulated);
      },
      onComplete: (fullResp) => {
        if (isFinished) return; // Strict duplicate guard
        isFinished = true;
        const finalText = fullResp || accumulated;
        setMessages((prev) => [...prev, { role: 'assistant', content: finalText }]);
        setStreamingText('');
        setOrbState('idle');
        speakText(finalText);
      },
      onError: (err) => {
        if (isFinished) return;
        isFinished = true;
        console.error('Streaming error:', err);
        const fallbackErr = 'Maaf kijiye, response lane me masla aaya. Barah-e-karam dobara koshish karein.';
        setMessages((prev) => [...prev, { role: 'assistant', content: fallbackErr }]);
        setStreamingText('');
        setOrbState('idle');
      }
    });
  };

  handleSendMessageRef.current = handleSendMessage;

  // Speech Recognition Setup (Web Speech API)
  useEffect(() => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SpeechRecognition) {
      const recognition = new SpeechRecognition();
      recognition.continuous = false;
      recognition.interimResults = true;
      recognition.lang = navigator.language || 'en-US';

      recognition.onstart = () => {
        setIsListening(true);
        setOrbState('listening');
        latestSpeechRef.current = '';
        setVoiceStatus('Listening to you... Speak now');
      };

      recognition.onresult = (event) => {
        let finalTranscript = '';
        let interimTranscript = '';
        for (let i = 0; i < event.results.length; ++i) {
          if (event.results[i].isFinal) {
            finalTranscript += event.results[i][0].transcript;
          } else {
            interimTranscript += event.results[i][0].transcript;
          }
        }
        const fullText = (finalTranscript || interimTranscript).trim();
        if (fullText) {
          latestSpeechRef.current = fullText;
          setTranscript(fullText);
          setInput(fullText);
        }
      };

      recognition.onerror = (event) => {
        console.warn('Speech recognition error:', event.error);
        setIsListening(false);
        setOrbState('idle');
        if (event.error === 'not-allowed') {
          setVoiceStatus('Microphone access blocked. Please enable mic permissions in your browser.');
        } else if (event.error === 'no-speech') {
          setVoiceStatus('No speech detected. Tap the mic to try again.');
        }
      };

      recognition.onend = () => {
        setIsListening(false);
        const spoken = latestSpeechRef.current.trim();
        latestSpeechRef.current = '';
        if (spoken) {
          setVoiceStatus('');
          handleSendMessageRef.current(spoken);
        } else {
          setOrbState((prev) => (prev === 'listening' ? 'idle' : prev));
        }
      };

      recognitionRef.current = recognition;
    }
  }, []);

  // Text-To-Speech Output
  const speakText = useCallback((text) => {
    if (!voiceOutputEnabled || !('speechSynthesis' in window)) return;
    try {
      window.speechSynthesis.cancel();
      // Clean markdown symbols for cleaner speech
      const cleanSpoken = text.replace(/[*_#`[\]()]/g, ' ').replace(/-/g, ' ');
      const utterance = new SpeechSynthesisUtterance(cleanSpoken);
      utterance.rate = 1.05;
      utterance.pitch = 1.0;
      utterance.onstart = () => setOrbState('speaking');
      utterance.onend = () => setOrbState('idle');
      window.speechSynthesis.speak(utterance);
    } catch (e) {
      console.warn('Speech synthesis error:', e);
    }
  }, [voiceOutputEnabled]);

  // Toggle Voice Listening
  const toggleVoiceInput = () => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      alert('Speech recognition is not supported in this browser. Please use Google Chrome, Microsoft Edge, or Safari.');
      return;
    }

    if (isListening) {
      if (recognitionRef.current) {
        try {
          recognitionRef.current.stop();
        } catch (e) {}
      }
      setIsListening(false);
      setOrbState('idle');
      setVoiceStatus('');
    } else {
      try {
        latestSpeechRef.current = '';
        setTranscript('');
        setVoiceStatus('Starting microphone...');
        recognitionRef.current?.start();
      } catch (err) {
        console.warn('Recognition start retry:', err);
        try {
          recognitionRef.current?.stop();
          setTimeout(() => recognitionRef.current?.start(), 150);
        } catch (e) {
          setVoiceStatus('Microphone is busy. Please try again.');
        }
      }
    }
  };

  const handleLogout = () => {
    if ('speechSynthesis' in window) window.speechSynthesis.cancel();
    localStorage.removeItem('token');
    navigate('/login');
  };

  const handleClearChat = () => {
    if ('speechSynthesis' in window) window.speechSynthesis.cancel();
    setMessages([
      {
        role: 'assistant',
        content: '✨ Chat cleared. How can I assist you with your shopping today?'
      }
    ]);
    setOrbState('idle');
  };

  // Helper to format assistant markdown nicely
  const formatContent = (text) => {
    if (!text) return null;
    return text.split('\n').map((line, idx) => {
      // Heading format
      if (line.startsWith('### ')) {
        return <h4 key={idx} className="text-base font-bold text-indigo-300 mt-2 mb-1">{line.replace('### ', '')}</h4>;
      }
      if (line.startsWith('## ') || line.startsWith('# ')) {
        return <h3 key={idx} className="text-lg font-bold text-white mt-2 mb-1">{line.replace(/^#+ /, '')}</h3>;
      }
      // Bullet list format
      if (line.trim().startsWith('- ') || line.trim().startsWith('* ')) {
        const itemText = line.trim().replace(/^[-*]\s+/, '');
        return (
          <div key={idx} className="flex items-start space-x-2 my-1 text-slate-200">
            <span className="text-indigo-400 mt-1 text-xs">◆</span>
            <span className="flex-1 leading-relaxed">{parseInlineMarkdown(itemText)}</span>
          </div>
        );
      }
      // Standard line
      return line ? <p key={idx} className="my-1 text-slate-200 leading-relaxed">{parseInlineMarkdown(line)}</p> : <div key={idx} className="h-2" />;
    });
  };

  // Simple inline markdown (bolding, price, stock highlights)
  const parseInlineMarkdown = (str) => {
    if (!str) return '';
    // Handle bold **text**
    const parts = str.split(/(\*\*.*?\*\*)/g);
    return parts.map((part, i) => {
      if (part.startsWith('**') && part.endsWith('**')) {
        const inner = part.slice(2, -2);
        // Highlight stock or status
        if (inner.toLowerCase().includes('in stock') || inner.toLowerCase().includes('available')) {
          return <span key={i} className="font-bold text-emerald-400 bg-emerald-950/60 px-1.5 py-0.5 rounded border border-emerald-800/50">{inner}</span>;
        }
        if (inner.startsWith('Order #') || inner.toLowerCase().includes('status')) {
          return <span key={i} className="font-bold text-amber-300 bg-amber-950/60 px-1.5 py-0.5 rounded border border-amber-800/50">{inner}</span>;
        }
        return <strong key={i} className="font-semibold text-white">{inner}</strong>;
      }
      return part;
    });
  };

  return (
    <div className="flex flex-col h-screen bg-slate-950 text-slate-100 font-sans relative overflow-hidden">
      {/* Background ambient lighting */}
      <div className="absolute -top-32 left-1/2 -translate-x-1/2 w-[600px] h-[350px] bg-gradient-to-b from-indigo-600/15 via-purple-600/10 to-transparent blur-3xl pointer-events-none"></div>

      {/* Top Navigation Bar */}
      <header className="h-16 border-b border-slate-800/80 bg-slate-900/40 backdrop-blur-xl px-6 flex items-center justify-between z-20">
        <div className="flex items-center space-x-3">
          <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-indigo-500 to-cyan-400 p-[1.5px] flex items-center justify-center shadow-md shadow-indigo-500/20">
            <div className="w-full h-full bg-slate-950 rounded-full flex items-center justify-center text-sm">
              ✨
            </div>
          </div>
          <div>
            <h1 className="text-sm font-bold text-white tracking-wide flex items-center gap-2">
              Nova Store AI
              <span className="text-[10px] bg-emerald-950/80 text-emerald-400 border border-emerald-800/60 px-2 py-0.5 rounded-full font-medium flex items-center gap-1">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
                In-Stock Live
              </span>
            </h1>
          </div>
        </div>

        {/* Action Controls */}
        <div className="flex items-center space-x-3">
          {/* Voice Output Toggle */}
          <button
            onClick={() => setVoiceOutputEnabled(!voiceOutputEnabled)}
            className={`px-3 py-1.5 rounded-xl text-xs font-medium border transition-all flex items-center gap-1.5 cursor-pointer ${
              voiceOutputEnabled 
                ? 'bg-indigo-600/20 text-indigo-300 border-indigo-500/50 shadow-sm shadow-indigo-500/20' 
                : 'bg-slate-800/60 text-slate-400 border-slate-700/60 hover:text-slate-200'
            }`}
            title="Toggle Voice Output (Speech)"
          >
            <span>{voiceOutputEnabled ? '🔊 Voice On' : '🔇 Voice Muted'}</span>
          </button>

          {/* Clear Chat */}
          <button
            onClick={handleClearChat}
            className="px-3 py-1.5 rounded-xl text-xs font-medium bg-slate-800/60 hover:bg-slate-700/60 text-slate-300 border border-slate-700/60 transition-all cursor-pointer"
            title="Clear Chat History"
          >
            Clear
          </button>

          {/* Logout */}
          <button
            onClick={handleLogout}
            className="px-3 py-1.5 rounded-xl text-xs font-medium bg-slate-800/60 hover:bg-red-950/40 text-slate-300 hover:text-red-300 border border-slate-700/60 hover:border-red-800/50 transition-all cursor-pointer"
          >
            Logout
          </button>
        </div>
      </header>

      {/* Main Center Area */}
      <main className="flex-1 flex flex-col max-w-4xl w-full mx-auto p-4 md:p-6 overflow-hidden relative z-10">
        
        {/* =========================================================================
            Centerpiece: The Graceful Glowing Rounded Ball (Listening Orb)
            ========================================================================= */}
        <div className="flex flex-col items-center justify-center py-4 select-none">
          <div className="relative flex items-center justify-center cursor-pointer group" onClick={toggleVoiceInput}>
            
            {/* Ripple Wave Rings when Listening / Speaking */}
            {orbState === 'listening' && (
              <>
                <div className="absolute w-36 h-36 rounded-full border border-pink-500/40 ripple-ring pointer-events-none"></div>
                <div className="absolute w-44 h-44 rounded-full border border-cyan-400/30 ripple-ring pointer-events-none" style={{ animationDelay: '0.6s' }}></div>
              </>
            )}
            {orbState === 'speaking' && (
              <div className="absolute w-36 h-36 rounded-full border border-emerald-400/40 ripple-ring pointer-events-none"></div>
            )}

            {/* Glowing Orb Body */}
            <div
              className={`w-20 h-20 md:w-24 md:h-24 rounded-full transition-all duration-500 flex items-center justify-center relative shadow-2xl ${
                orbState === 'idle'
                  ? 'orb-idle bg-gradient-to-tr from-indigo-600 via-purple-600 to-cyan-400 shadow-indigo-500/40'
                  : orbState === 'listening'
                  ? 'orb-listening bg-gradient-to-tr from-pink-600 via-purple-600 to-cyan-300 shadow-pink-500/60'
                  : orbState === 'thinking'
                  ? 'orb-thinking bg-gradient-to-tr from-cyan-400 via-indigo-600 to-pink-500 shadow-cyan-500/50'
                  : 'orb-speaking bg-gradient-to-tr from-emerald-500 via-cyan-500 to-indigo-600 shadow-emerald-500/50'
              }`}
            >
              {/* Inner Glossy Glass Sphere Overlay */}
              <div className="w-[90%] h-[90%] rounded-full bg-slate-950/40 backdrop-blur-sm border border-white/25 flex flex-col items-center justify-center">
                {/* Visual Icon / State Indicator inside Ball */}
                {orbState === 'idle' && <span className="text-xl md:text-2xl filter drop-shadow">✨</span>}
                {orbState === 'listening' && <span className="text-xl md:text-2xl text-white animate-pulse">🎙️</span>}
                {orbState === 'thinking' && <span className="text-xl md:text-2xl text-cyan-300 animate-spin">✦</span>}
                {orbState === 'speaking' && <span className="text-xl md:text-2xl text-emerald-300">💬</span>}
              </div>
            </div>
          </div>

          {/* Orb Status Label & Audio Visualizer Bars */}
          <div className="mt-3 text-center flex flex-col items-center">
            <p className="text-xs font-semibold tracking-wider text-slate-300 flex items-center gap-1.5">
              {voiceStatus ? (
                <span className="text-pink-400 font-bold flex items-center gap-1.5 animate-pulse">
                  <span className="w-2 h-2 rounded-full bg-pink-500 animate-ping"></span>
                  {voiceStatus}
                </span>
              ) : orbState === 'idle' ? (
                <span className="text-slate-400 hover:text-indigo-300 transition-colors">
                  Tap orb or mic to speak • Ready
                </span>
              ) : orbState === 'listening' ? (
                <span className="text-pink-400 font-bold flex items-center gap-1">
                  <span className="w-2 h-2 rounded-full bg-pink-500 animate-ping"></span>
                  Listening to you... Speak now
                </span>
              ) : orbState === 'thinking' ? (
                <span className="text-cyan-400 font-medium flex items-center gap-1.5">
                  <span className="w-1.5 h-1.5 rounded-full bg-cyan-400 animate-ping"></span>
                  Checking store stock & searching...
                </span>
              ) : (
                <span className="text-emerald-400 font-medium">
                  Nova is responding in real-time...
                </span>
              )}
            </p>

            {/* Audio Wave Visualizer Bars when active */}
            {(orbState === 'listening' || orbState === 'speaking') && (
              <div className="flex items-center justify-center space-x-1.5 h-6 mt-1">
                {[0, 1, 2, 3, 4, 5, 6].map((i) => (
                  <div
                    key={i}
                    className={`w-1 rounded-full wave-bar-anim ${
                      orbState === 'listening' ? 'bg-pink-400' : 'bg-emerald-400'
                    }`}
                    style={{ animationDelay: `${i * 120}ms` }}
                  />
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Quick Suggestion Chips */}
        <div className="flex items-center gap-2 overflow-x-auto pb-2 scrollbar-none justify-start md:justify-center my-1">
          {QUICK_PROMPTS.map((item, idx) => (
            <button
              key={idx}
              onClick={() => handleSendMessage(item.query)}
              disabled={orbState === 'thinking' || orbState === 'speaking'}
              className="text-xs whitespace-nowrap bg-slate-900/90 hover:bg-indigo-950/60 text-slate-300 hover:text-indigo-200 border border-slate-800 hover:border-indigo-700/60 px-3 py-1.5 rounded-full transition-all cursor-pointer active:scale-95 disabled:opacity-40"
            >
              {item.label}
            </button>
          ))}
        </div>

        {/* =========================================================================
            Message History & Real-Time Stream Box
            ========================================================================= */}
        <div className="flex-1 overflow-y-auto pr-2 space-y-4 my-2 scrollbar-thin">
          {messages.map((msg, index) => (
            <div
              key={index}
              className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-[85%] md:max-w-[80%] px-4 py-3 rounded-2xl text-sm shadow-lg leading-relaxed ${
                  msg.role === 'user'
                    ? 'bg-gradient-to-r from-indigo-600 to-indigo-700 text-white rounded-br-none border border-indigo-500/30'
                    : 'bg-slate-900/90 border border-slate-800/90 text-slate-200 rounded-bl-none'
                }`}
              >
                {msg.role === 'assistant' && (
                  <div className="flex items-center justify-between text-xs text-indigo-400 font-semibold mb-1 pb-1 border-b border-slate-800/60">
                    <span className="flex items-center gap-1">✨ Nova Assistant</span>
                  </div>
                )}
                <div>{formatContent(msg.content)}</div>
              </div>
            </div>
          ))}

          {/* Active Real-Time Stream Output */}
          {streamingText && (
            <div className="flex justify-start">
              <div className="max-w-[85%] md:max-w-[80%] px-4 py-3 rounded-2xl rounded-bl-none text-sm shadow-lg bg-slate-900/95 border border-indigo-500/40 text-slate-200 leading-relaxed relative">
                <div className="flex items-center text-xs text-cyan-400 font-semibold mb-1 pb-1 border-b border-slate-800/60">
                  <span className="flex items-center gap-1">
                    <span className="w-1.5 h-1.5 rounded-full bg-cyan-400 animate-ping"></span>
                    Streaming Response...
                  </span>
                </div>
                <div>{formatContent(streamingText)}</div>
                <span className="inline-block w-2 h-4 bg-indigo-400 animate-pulse ml-1 align-middle"></span>
              </div>
            </div>
          )}

          {/* Thinking indicator before first token */}
          {orbState === 'thinking' && !streamingText && (
            <div className="flex justify-start">
              <div className="bg-slate-900/80 border border-slate-800 px-4 py-3 rounded-2xl rounded-bl-none shadow-md flex items-center space-x-2 text-xs text-slate-400">
                <span className="w-2 h-2 rounded-full bg-indigo-400 animate-bounce"></span>
                <span className="w-2 h-2 rounded-full bg-purple-400 animate-bounce" style={{ animationDelay: '150ms' }}></span>
                <span className="w-2 h-2 rounded-full bg-cyan-400 animate-bounce" style={{ animationDelay: '300ms' }}></span>
                <span className="text-slate-400 font-medium ml-1">Searching store inventory...</span>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* =========================================================================
            Floating Input Bar with Voice Button & Send
            ========================================================================= */}
        <div className="pt-2">
          <form
            onSubmit={(e) => {
              e.preventDefault();
              handleSendMessage();
            }}
            className="flex items-center bg-slate-900/90 border border-slate-800 focus-within:border-indigo-500/80 rounded-2xl px-3 py-2 transition-all shadow-xl shadow-black/40 backdrop-blur-md"
          >
            {/* Microphone Button */}
            <button
              type="button"
              onClick={toggleVoiceInput}
              className={`p-2.5 rounded-xl transition-all cursor-pointer flex items-center justify-center ${
                isListening
                  ? 'bg-pink-600 text-white shadow-lg shadow-pink-600/30 animate-pulse'
                  : 'bg-slate-800/80 hover:bg-slate-700/80 text-slate-300 hover:text-white'
              }`}
              title={isListening ? 'Stop Listening' : 'Click to Speak (Voice Input)'}
            >
              <span className="text-sm">🎙️</span>
            </button>

            {/* Input Text Box */}
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              disabled={orbState === 'thinking' || orbState === 'speaking'}
              placeholder={
                isListening
                  ? 'Listening to you... Speak now'
                  : 'Ask about any product, check stock, or track order #1001...'
              }
              className="flex-1 bg-transparent text-white focus:outline-none text-sm px-3 placeholder-slate-500"
            />

            {/* Send Button */}
            <button
              type="submit"
              disabled={!input.trim() || orbState === 'thinking' || orbState === 'speaking'}
              className="bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 disabled:opacity-30 text-white px-4 py-2 rounded-xl text-xs font-semibold tracking-wider transition-all shadow-md shadow-indigo-600/20 active:scale-95 cursor-pointer disabled:cursor-not-allowed"
            >
              Send
            </button>
          </form>
        </div>

      </main>
    </div>
  );
}