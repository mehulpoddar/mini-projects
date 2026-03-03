/* ===== Guesspionage Game Engine ===== */

const TEAM_COLORS = [
  'var(--team1)', 'var(--team2)', 'var(--team3)',
  'var(--team4)', 'var(--team5)', 'var(--team6)'
];

const MAX_QUESTIONS = 2;

const SCORING = {
  GUESS_TIERS: [
    { maxDiff: 0,  points: 5000 },
    { maxDiff: 5,  points: 4000 },
    { maxDiff: 10, points: 2000 },
    { maxDiff: 15, points: 1000 },
    { maxDiff: 25, points: 500  },
    { maxDiff: 35, points: 500  },
  ],
  HIGHER_LOWER_CORRECT: 1000
};

// ===== State =====
let questions = [];
let teams = [];
let currentRound = 0;
let activeTeamIndex = 0;
let currentGuess = 50;
let votes = {}; // { teamIndex: 'higher' | 'lower' }
let shuffledQuestions = [];

// ===== DOM refs =====
const $ = (sel) => document.querySelector(sel);
const $$ = (sel) => document.querySelectorAll(sel);

// ===== Init =====
document.addEventListener('DOMContentLoaded', () => {
  questions = QUESTIONS_DATA;
  bindEvents();
});

function bindEvents() {
  $('#btn-start').addEventListener('click', () => switchScreen('screen-setup'));
  $('#btn-add-team').addEventListener('click', addTeamInput);
  $('#btn-remove-team').addEventListener('click', removeTeamInput);
  $('#btn-begin').addEventListener('click', beginGame);
  $('#btn-show-guess').addEventListener('click', () => switchScreen('screen-guess'));
  $('#guess-slider').addEventListener('input', onSliderChange);
  $('#btn-lock-guess').addEventListener('click', lockGuess);
  $('#btn-reveal').addEventListener('click', revealAnswer);
  $('#btn-next-round').addEventListener('click', showScoreboard);
  $('#btn-continue').addEventListener('click', nextRound);
  $('#btn-play-again').addEventListener('click', resetGame);
}

// ===== Screen Management =====
function switchScreen(screenId) {
  $$('.screen').forEach(s => s.classList.remove('active'));
  const target = $(`#${screenId}`);
  target.classList.add('active');
  // Re-trigger animation
  target.style.animation = 'none';
  target.offsetHeight; // reflow
  target.style.animation = '';
}

// ===== Team Setup =====
function getTeamCount() {
  return $$('.team-input-row').length;
}

function addTeamInput() {
  const count = getTeamCount();
  if (count >= 6) return;
  const row = document.createElement('div');
  row.className = 'team-input-row';
  row.innerHTML = `
    <span class="team-color-dot" style="background:${TEAM_COLORS[count]}"></span>
    <input type="text" class="team-name-input" placeholder="Team ${count + 1}" maxlength="20">
  `;
  $('#team-inputs').appendChild(row);
  updateRemoveBtn();
}

function removeTeamInput() {
  const count = getTeamCount();
  if (count <= 2) return;
  $('#team-inputs').lastElementChild.remove();
  updateRemoveBtn();
}

function updateRemoveBtn() {
  $('#btn-remove-team').style.display = getTeamCount() <= 2 ? 'none' : '';
  $('#btn-add-team').style.display = getTeamCount() >= 6 ? 'none' : '';
}

// ===== Begin Game =====
function beginGame() {
  const inputs = $$('.team-name-input');
  teams = [];
  inputs.forEach((input, i) => {
    const name = input.value.trim() || `Team ${i + 1}`;
    teams.push({ name, score: 0, color: TEAM_COLORS[i] });
  });

  if (teams.length < 2) return;

  // Shuffle questions
  shuffledQuestions = [...questions].sort(() => Math.random() - 0.5).slice(0, MAX_QUESTIONS);
  currentRound = 0;
  activeTeamIndex = 0;

  startRound();
}

// ===== Round Flow =====
function startRound() {
  if (currentRound >= shuffledQuestions.length) {
    showFinalResults();
    return;
  }

  const q = shuffledQuestions[currentRound];
  votes = {};
  currentGuess = 50;

  // Update HUD across screens
  const roundNum = currentRound + 1;
  const totalRounds = shuffledQuestions.length;
  const activeTeam = teams[activeTeamIndex];

  $$('[id^="hud-round-num"]').forEach(el => el.textContent = roundNum);
  $$('[id^="hud-total-rounds"]').forEach(el => el.textContent = totalRounds);
  $$('[id^="hud-active-team"]').forEach(el => {
    el.textContent = activeTeam.name;
    el.style.color = activeTeam.color;
  });

  // Question screen
  $('#question-category').textContent = q.category;
  $('#question-text').textContent = q.question;

  // Reset slider
  $('#guess-slider').value = 50;
  $('#slider-value').textContent = '50%';

  switchScreen('screen-question');
}

function onSliderChange(e) {
  currentGuess = parseInt(e.target.value);
  const display = $('#slider-value');
  display.textContent = `${currentGuess}%`;

  // Color shift based on value
  if (currentGuess <= 25) display.style.color = 'var(--red)';
  else if (currentGuess <= 50) display.style.color = 'var(--orange)';
  else if (currentGuess <= 75) display.style.color = 'var(--gold)';
  else display.style.color = 'var(--green)';
}

function lockGuess() {
  // Build vote screen
  const activeTeam = teams[activeTeamIndex];
  $('#vote-team-name').textContent = activeTeam.name;
  $('#vote-team-name').style.color = activeTeam.color;
  $('#vote-guess-display').textContent = `${currentGuess}%`;

  const voteContainer = $('#vote-teams');
  voteContainer.innerHTML = '';

  teams.forEach((team, i) => {
    if (i === activeTeamIndex) return; // skip active team
    const row = document.createElement('div');
    row.className = 'vote-team-row';
    row.style.animationDelay = `${i * 0.1}s`;
    row.innerHTML = `
      <span class="team-color-dot" style="background:${team.color}"></span>
      <span class="vote-team-name" style="color:${team.color}">${team.name}</span>
      <div class="vote-buttons">
        <button class="vote-btn" data-team="${i}" data-vote="higher">⬆ Higher</button>
        <button class="vote-btn" data-team="${i}" data-vote="lower">⬇ Lower</button>
      </div>
    `;
    voteContainer.appendChild(row);
  });

  // Bind vote buttons
  voteContainer.querySelectorAll('.vote-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const teamIdx = parseInt(btn.dataset.team);
      const vote = btn.dataset.vote;

      // Deselect sibling
      const siblings = btn.parentElement.querySelectorAll('.vote-btn');
      siblings.forEach(s => s.classList.remove('selected-higher', 'selected-lower'));

      btn.classList.add(vote === 'higher' ? 'selected-higher' : 'selected-lower');
      votes[teamIdx] = vote;
    });
  });

  switchScreen('screen-vote');
}

// ===== Reveal =====
function revealAnswer() {
  const q = shuffledQuestions[currentRound];
  const answer = q.answer;
  const diff = Math.abs(currentGuess - answer);
  const activeTeam = teams[activeTeamIndex];

  // Populate reveal screen
  $('#reveal-question').textContent = q.question;
  $('#reveal-guess').textContent = `${currentGuess}%`;
  $('#reveal-answer').textContent = `${answer}%`;

  // Bars
  $('#reveal-bar-guess').style.width = `${currentGuess}%`;
  $('#reveal-bar-answer').style.width = `${answer}%`;
  $('#reveal-bar-marker-guess').style.left = `${currentGuess}%`;
  $('#reveal-bar-marker-answer').style.left = `${answer}%`;

  // Fun fact
  $('#fun-fact-text').textContent = q.funFact;
  if (q.source) {
    $('#fun-fact-source').textContent = `Source: ${q.source}`;
    $('#fun-fact-source').style.display = '';
  } else {
    $('#fun-fact-source').style.display = 'none';
  }

  // Calculate scores
  let activePoints = 0;
  for (const tier of SCORING.GUESS_TIERS) {
    if (diff <= tier.maxDiff) { activePoints = tier.points; break; }
  }

  teams[activeTeamIndex].score += activePoints;

  // Higher/Lower scoring
  const roundScoresEl = $('#round-scores');
  roundScoresEl.innerHTML = '';
  const roundDeltas = [];

  // Active team chip
  roundDeltas.push({ name: activeTeam.name, color: activeTeam.color, delta: activePoints });

  // Other teams
  teams.forEach((team, i) => {
    if (i === activeTeamIndex) return;
    let pts = 0;
    if (votes[i]) {
      const isHigher = answer > currentGuess;
      const isLower = answer < currentGuess;
      const isExact = answer === currentGuess;

      if (isExact) {
        // If guess was exact, no one gets higher/lower points
        pts = 0;
      } else if ((votes[i] === 'higher' && isHigher) || (votes[i] === 'lower' && isLower)) {
        pts = SCORING.HIGHER_LOWER_CORRECT;
      }
    }
    teams[i].score += pts;
    roundDeltas.push({ name: team.name, color: team.color, delta: pts });
  });

  // Render round score chips
  roundDeltas.forEach((d, i) => {
    const chip = document.createElement('div');
    chip.className = 'round-score-chip';
    chip.style.animationDelay = `${0.6 + i * 0.15}s`;
    chip.innerHTML = `
      <span class="team-color-dot" style="background:${d.color}"></span>
      <span>${d.name}</span>
      <span class="score-delta ${d.delta === 0 ? 'zero' : ''}">+${d.delta}</span>
    `;
    roundScoresEl.appendChild(chip);
  });

  // Color the guess based on accuracy
  const guessEl = $('#reveal-guess');
  if (diff === 0) { guessEl.style.color = 'var(--green)'; }
  else if (diff <= 10) { guessEl.style.color = 'var(--green)'; }
  else if (diff <= 25) { guessEl.style.color = 'var(--gold)'; }
  else { guessEl.style.color = 'var(--red)'; }

  switchScreen('screen-reveal');
}

// ===== Scoreboard =====
function showScoreboard() {
  renderScoreboard($('#scoreboard-list'));
  switchScreen('screen-scoreboard');
}

function renderScoreboard(container) {
  const sorted = teams.map((t, i) => ({ ...t, index: i }))
    .sort((a, b) => b.score - a.score);

  container.innerHTML = '';
  sorted.forEach((team, rank) => {
    const row = document.createElement('div');
    row.className = `scoreboard-row ${rank === 0 ? 'rank-1' : ''}`;
    row.style.animationDelay = `${rank * 0.1}s`;
    row.innerHTML = `
      <span class="scoreboard-rank">${rank === 0 ? '👑' : '#' + (rank + 1)}</span>
      <span class="team-color-dot" style="background:${team.color}"></span>
      <span class="scoreboard-name">${team.name}</span>
      <span class="scoreboard-score">${team.score.toLocaleString()}</span>
    `;
    container.appendChild(row);
  });
}

function nextRound() {
  currentRound++;
  activeTeamIndex = (activeTeamIndex + 1) % teams.length;
  startRound();
}

// ===== Final Results =====
function showFinalResults() {
  const sorted = [...teams].sort((a, b) => b.score - a.score);
  const winner = sorted[0];

  $('#final-winner').textContent = `${winner.name} wins!`;
  $('#final-winner').style.color = winner.color;

  renderScoreboard($('#final-scoreboard'));
  switchScreen('screen-final');
  launchConfetti();
}

// ===== Confetti =====
function launchConfetti() {
  const wrapper = $('#confetti-wrapper');
  wrapper.innerHTML = '';
  const colors = ['#ff6b6b', '#48dbfb', '#feca57', '#ff9ff3', '#54a0ff', '#5f27cd', '#00e676', '#ffd740'];

  for (let i = 0; i < 80; i++) {
    const piece = document.createElement('div');
    piece.className = 'confetti-piece';
    piece.style.left = `${Math.random() * 100}%`;
    piece.style.background = colors[Math.floor(Math.random() * colors.length)];
    piece.style.width = `${6 + Math.random() * 10}px`;
    piece.style.height = `${6 + Math.random() * 10}px`;
    piece.style.borderRadius = Math.random() > 0.5 ? '50%' : '2px';
    piece.style.animationDuration = `${2 + Math.random() * 3}s`;
    piece.style.animationDelay = `${Math.random() * 2}s`;
    wrapper.appendChild(piece);
  }

  // Clean up after animation
  setTimeout(() => { wrapper.innerHTML = ''; }, 6000);
}

// ===== Reset =====
function resetGame() {
  teams.forEach(t => t.score = 0);
  currentRound = 0;
  activeTeamIndex = 0;
  votes = {};
  shuffledQuestions = [...questions].sort(() => Math.random() - 0.5);
  switchScreen('screen-title');
}
