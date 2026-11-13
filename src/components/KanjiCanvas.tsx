import React, { useRef, useState, useEffect, useCallback } from 'react';
import { Volume2 } from 'lucide-react';
import type { CharacterStrokeData } from '../types/kanji';

interface KanjiCanvasProps {
  characters: CharacterStrokeData[];
  initialHinted: boolean;
  showGuideLines: boolean;
  practiceMode?: boolean;
  onPlayAudio?: () => void;
  onComplete?: () => void;
}

export const KanjiCanvas: React.FC<KanjiCanvasProps> = ({
  characters,
  initialHinted,
  showGuideLines,
  practiceMode = false,
  onPlayAudio,
  onComplete,
}) => {
  const [charIndex, setCharIndex] = useState(0);
  const [strokeIndex, setStrokeIndex] = useState(0);
  const [hintVisible, setHintVisible] = useState(initialHinted);
  const [isFinished, setIsFinished] = useState(false);
  const [userPoints, setUserPoints] = useState<{ x: number; y: number }[]>([]);
  const [isDrawing, setIsDrawing] = useState(false);
  const [strokeEndpoint, setStrokeEndpoint] = useState<{
    start: { x: number; y: number };
    end: { x: number; y: number };
  } | null>(null);

  const svgRef = useRef<SVGSVGElement | null>(null);
  const activePathRef = useRef<SVGPathElement | null>(null);

  const currentChar = characters[charIndex] || characters[0];
  const currentStrokeD = currentChar?.strokes[strokeIndex] || '';

  const resetCanvas = useCallback(() => {
    setCharIndex(0);
    setStrokeIndex(0);
    setHintVisible(practiceMode ? true : initialHinted);
    setIsFinished(false);
    setUserPoints([]);
    setIsDrawing(false);
  }, [initialHinted, practiceMode]);

  useEffect(() => {
    resetCanvas();
  }, [characters, resetCanvas]);

  useEffect(() => {
    if (!activePathRef.current || !currentStrokeD) {
      setStrokeEndpoint(null);
      return;
    }
    try {
      const totalLen = activePathRef.current.getTotalLength();
      const startPt = activePathRef.current.getPointAtLength(0);
      const endPt = activePathRef.current.getPointAtLength(totalLen);
      setStrokeEndpoint({
        start: { x: startPt.x, y: startPt.y },
        end: { x: endPt.x, y: endPt.y },
      });
    } catch {
      setStrokeEndpoint(null);
    }
  }, [currentStrokeD, charIndex, strokeIndex]);

  const toSvgCoords = (clientX: number, clientY: number) => {
    const svg = svgRef.current;
    if (!svg) return { x: 0, y: 0 };
    const rect = svg.getBoundingClientRect();
    return {
      x: ((clientX - rect.left) / rect.width) * 109,
      y: ((clientY - rect.top) / rect.height) * 109,
    };
  };

  const handlePointerDown = (e: React.PointerEvent<SVGSVGElement>) => {
    if (isFinished) return;
    e.currentTarget.setPointerCapture(e.pointerId);
    const pt = toSvgCoords(e.clientX, e.clientY);
    setIsDrawing(true);
    setUserPoints([pt]);
  };

  const handlePointerMove = (e: React.PointerEvent<SVGSVGElement>) => {
    if (!isDrawing || isFinished) return;
    const pt = toSvgCoords(e.clientX, e.clientY);
    setUserPoints((prev) => [...prev, pt]);
  };

  const validateAndAdvance = useCallback(
    (points: { x: number; y: number }[]) => {
      if (points.length < 2 || !strokeEndpoint) return;

      const userStart = points[0];
      const userEnd = points[points.length - 1];

      const distStart = Math.hypot(
        userStart.x - strokeEndpoint.start.x,
        userStart.y - strokeEndpoint.start.y
      );
      const distEnd = Math.hypot(
        userEnd.x - strokeEndpoint.end.x,
        userEnd.y - strokeEndpoint.end.y
      );

      if (distStart <= 25 && distEnd <= 25) {
        const nextStroke = strokeIndex + 1;
        if (nextStroke < currentChar.strokes.length) {
          setStrokeIndex(nextStroke);
        } else {
          const nextChar = charIndex + 1;
          if (nextChar < characters.length) {
            setCharIndex(nextChar);
            setStrokeIndex(0);
          } else {
            setIsFinished(true);
          }
        }
      }
    },
    [strokeEndpoint, strokeIndex, currentChar, charIndex, characters.length]
  );

  const handlePointerUp = () => {
    if (!isDrawing) return;
    setIsDrawing(false);
    validateAndAdvance(userPoints);
    setUserPoints([]);
  };

  const livePolyline = userPoints.map((p) => `${p.x},${p.y}`).join(' ');

  return (
    <div className="flex flex-col items-center w-full">
      {/* Multi-character badge indicator for compounds in lessons */}
      {!practiceMode && characters.length > 1 && (
        <div className="flex gap-2 mb-3">
          {characters.map((c, idx) => (
            <span
              key={idx}
              className={`px-2.5 py-0.5 rounded text-sm font-medium ${
                idx < charIndex || isFinished
                  ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/40'
                  : idx === charIndex
                  ? 'bg-sky-500/20 text-sky-300 border border-sky-400'
                  : 'bg-slate-700/50 text-slate-400'
              }`}
            >
              {idx < charIndex || isFinished ? c.char : `Char ${idx + 1}`}
            </span>
          ))}
        </div>
      )}

      {/* Drawing Box */}
      <div className="relative w-72 h-72 sm:w-80 sm:h-80 bg-[#3B4252] rounded-xl border border-slate-500/40 shadow-inner touch-none select-none">
        <svg
          ref={svgRef}
          viewBox="0 0 109 109"
          className="w-full h-full cursor-crosshair"
          onPointerDown={handlePointerDown}
          onPointerMove={handlePointerMove}
          onPointerUp={handlePointerUp}
        >
          {/* Optional Writing Guide Lines */}
          {showGuideLines && (
            <g stroke="#64748B" strokeWidth="0.6" strokeDasharray="3,3" opacity="0.55">
              <line x1="54.5" y1="0" x2="54.5" y2="109" />
              <line x1="0" y1="54.5" x2="109" y2="54.5" />
            </g>
          )}

          {/* Full Ghost Silhouette in Practice Mode (matches screenshot) */}
          {practiceMode &&
            currentChar.strokes.map((d, i) => (
              <path
                key={`ghost-${i}`}
                d={d}
                fill="none"
                stroke="#646D7E"
                strokeWidth="6.5"
                strokeLinecap="round"
                strokeLinejoin="round"
                opacity="0.45"
              />
            ))}

          {/* Hidden reference path for measuring start/end points */}
          {currentStrokeD && (
            <path ref={activePathRef} d={currentStrokeD} fill="none" stroke="none" />
          )}

          {/* Completed strokes in crisp white */}
          {currentChar.strokes
            .slice(0, isFinished ? currentChar.strokes.length : strokeIndex)
            .map((d, i) => (
              <path
                key={i}
                d={d}
                fill="none"
                stroke="#FFFFFF"
                strokeWidth="6"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            ))}

          {/* Current Stroke Hint (grey path + green start dot + red end dot) */}
          {!isFinished && hintVisible && currentStrokeD && (
            <g>
              <path
                d={currentStrokeD}
                fill="none"
                stroke="#8892A4"
                strokeWidth="6.5"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
              {strokeEndpoint && (
                <>
                  <circle
                    cx={strokeEndpoint.start.x}
                    cy={strokeEndpoint.start.y}
                    r="2.4"
                    fill="#22C55E"
                  />
                  <circle
                    cx={strokeEndpoint.end.x}
                    cy={strokeEndpoint.end.y}
                    r="2.4"
                    fill="#EF4444"
                  />
                </>
              )}
            </g>
          )}

          {/* Active User Brush Stroke */}
          {userPoints.length > 1 && (
            <polyline
              points={livePolyline}
              fill="none"
              stroke="#FFFFFF"
              strokeWidth="5.5"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          )}
        </svg>
      </div>

      {/* Practice Mode shows compact 'Reset' button directly underneath */}
      {practiceMode ? (
        <button
          type="button"
          onClick={resetCanvas}
          className="mt-5 px-9 py-2.5 rounded-lg bg-[#3B4252] hover:bg-[#464F62] text-white font-semibold text-sm shadow transition"
        >
          Reset
        </button>
      ) : (
        <>
          {onPlayAudio && (
            <button
              type="button"
              onClick={onPlayAudio}
              aria-label="Play pronunciation"
              className="mt-7 w-14 h-14 rounded-full bg-[#5DA9E9] hover:bg-[#4A96D6] active:scale-95 flex items-center justify-center text-white shadow-md transition"
            >
              <Volume2 className="w-7 h-7 fill-white" />
            </button>
          )}

          <div className="w-full max-w-md mt-6 px-4">
            {isFinished ? (
              <button
                type="button"
                onClick={onComplete}
                className="w-full py-3.5 rounded-xl bg-[#2ECC71] hover:bg-[#27AE60] text-white font-semibold text-lg shadow-md transition"
              >
                OK
              </button>
            ) : !hintVisible ? (
              <button
                type="button"
                onClick={() => setHintVisible(true)}
                className="w-full py-3.5 rounded-xl bg-[#F59E0B] hover:bg-[#D97706] text-white font-semibold text-lg shadow-md transition"
              >
                Show Hint
              </button>
            ) : (
              <div className="h-[52px]" />
            )}
          </div>
        </>
      )}
    </div>
  );
};