import React from 'react';
import { Activity, ShieldAlert, ShieldCheck } from 'lucide-react';

export default function Dashboard() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold tracking-tight text-white">Security Posture Dashboard</h1>
        <p className="text-sm text-gray-400 mt-1">
          Consolidated cryptographic posture metrics and standards compliance overview.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="border border-gray-800 bg-gray-900/40 p-5 rounded-lg">
          <div className="flex items-center justify-between">
            <span className="text-xs font-mono uppercase text-gray-400">Cryptographic Score</span>
            <ShieldCheck className="w-4 h-4 text-gray-500" />
          </div>
          <div className="mt-3 flex items-baseline gap-2">
            <span className="text-3xl font-bold font-mono text-gray-400">--</span>
            <span className="text-xs text-gray-500">/ 100</span>
          </div>
          <p className="text-xs text-gray-500 mt-2">No analysis available</p>
        </div>

        <div className="border border-gray-800 bg-gray-900/40 p-5 rounded-lg">
          <div className="flex items-center justify-between">
            <span className="text-xs font-mono uppercase text-gray-400">Active Sessions</span>
            <Activity className="w-4 h-4 text-gray-500" />
          </div>
          <div className="mt-3">
            <span className="text-3xl font-bold font-mono text-gray-400">0</span>
          </div>
          <p className="text-xs text-gray-500 mt-2">0 active sessions</p>
        </div>

        <div className="border border-gray-800 bg-gray-900/40 p-5 rounded-lg">
          <div className="flex items-center justify-between">
            <span className="text-xs font-mono uppercase text-gray-400">Identified Findings</span>
            <ShieldAlert className="w-4 h-4 text-gray-500" />
          </div>
          <div className="mt-3">
            <span className="text-3xl font-bold font-mono text-gray-400">0</span>
          </div>
          <p className="text-xs text-gray-500 mt-2">No analysis available</p>
        </div>
      </div>

      <div className="border border-gray-800 bg-gray-950/60 rounded-xl p-8 text-center text-xs font-mono text-gray-500">
        Data will appear after an analysis run has completed.
      </div>
    </div>
  );
}