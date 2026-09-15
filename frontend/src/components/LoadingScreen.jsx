import React from 'react';
import { Loader2 } from 'lucide-react';

export default function LoadingScreen({ message = 'Loading forensic telemetry...' }) {
  return (
    <div className="flex flex-col items-center justify-center p-12 text-gray-400 space-y-3">
      <Loader2 className="w-8 h-8 animate-spin text-blue-500" />
      <span className="text-xs font-mono tracking-wide">{message}</span>
    </div>
  );
}