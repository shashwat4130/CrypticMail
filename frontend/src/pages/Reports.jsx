import React from 'react';
import { FileText } from 'lucide-react';

export default function Reports() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold tracking-tight text-white">Forensic Reports</h1>
        <p className="text-sm text-gray-400 mt-1">
          Audit exports and machine-readable evidence packages.
        </p>
      </div>

      <div className="border border-gray-800 bg-gray-950/60 rounded-xl p-12 text-center">
        <FileText className="w-8 h-8 text-gray-600 mx-auto mb-3" />
        <p className="text-sm text-gray-300">
          Reports will be generated upon completion of an audit run
        </p>
        <p className="text-xs text-gray-500 mt-1 font-mono">
          Artifacts (PDF, JSON) will populate once an assessment job concludes.
        </p>
      </div>
    </div>
  );
}