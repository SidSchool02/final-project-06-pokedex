(() => {
	const form = document.getElementById("search-form");
	const input = document.getElementById("name-input");
	const errorEl = document.getElementById("error");
	const resultEl = document.getElementById("result");
	const cardTemplate = document.getElementById("card-template");

	const typeBorderColors = {
		normal: '#A8A878',
		fire: '#F08030',
		water: '#6890F0',
		electric: '#F8D030',
		grass: '#78C850',
		ice: '#98D8D8',
		fighting: '#C03028',
		poison: '#A040A0',
		ground: '#E0C068',
		flying: '#A890F0',
		psychic: '#F85888',
		bug: '#A8B820',
		rock: '#B8A038',
		ghost: '#705898',
		dragon: '#7038F8',
		dark: '#705848',
		steel: '#B8B8D0',
		fairy: '#EE99AC'
	};

	function showError(message) {
		errorEl.textContent = message;
		errorEl.classList.remove("hidden");
		resultEl.classList.add("hidden");
	}

	function clearError() {
		errorEl.classList.add("hidden");
		errorEl.textContent = "";
	}

	function renderResult(data) {
		const cardClone = cardTemplate.content.cloneNode(true);
		const card = cardClone.querySelector('.pokemon-card');
		const mainType = data.types?.[0]?.toLowerCase() || 'normal';
		card.setAttribute('data-main-type', mainType);
		card.style.borderColor = typeBorderColors[mainType] || '#ffd700';

		card.querySelector('.pokemon-name').textContent = data.name || "Unknown";
		const hp = data.hp || (data.id || 1) * 10;
		card.querySelector('.pokemon-hp').innerHTML = `${hp} <span>HP</span>`;
		const formattedId = String(data.id || 0).padStart(3, '0');
		card.querySelector('.pokemon-id-badge').textContent = `#${formattedId}`;

		const imgEl = card.querySelector('.card-image-container img');
		let imageUrl = data.images?.official_artwork ||
			data.images?.front_default ||
			data.sprites?.other?.['official-artwork']?.front_default ||
			data.sprites?.front_default ||
			`https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/${data.id}.png`;
		imgEl.src = imageUrl;
		imgEl.alt = data.name || "Pokemon";
		imgEl.onerror = function () {
			this.src = `https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/${data.id}.png`;
		};

		const typesContainer = card.querySelector('.pokemon-types');
		typesContainer.innerHTML = '';
		data.types?.forEach(type => {
			const typeSpan = document.createElement('span');
			typeSpan.className = `type ${type.toLowerCase()}`;
			typeSpan.textContent = type.charAt(0).toUpperCase() + type.slice(1);
			typesContainer.appendChild(typeSpan);
		});

		const abilitiesContainer = card.querySelector('.ability-list');
		abilitiesContainer.innerHTML = '';
		data.abilities?.forEach(ability => {
			const abilityItem = document.createElement('div');
			abilityItem.className = 'ability-item';
			abilityItem.innerHTML = `
				<div class="ability-icon">⭐</div>
				<span class="ability-name">${ability.name}</span>
				${ability.is_hidden ? '<span class="ability-hidden">Hidden</span>' : ''}
			`;
			abilitiesContainer.appendChild(abilityItem);
		});

		resultEl.innerHTML = '';
		resultEl.appendChild(cardClone);
		resultEl.classList.remove("hidden");
	}

	form.addEventListener("submit", async (e) => {
		e.preventDefault();
		const name = (input.value || "").trim();
		if (!name) {
			showError("Please enter a Pokémon name.");
			return;
		}
		clearError();
		resultEl.classList.add("hidden");
		resultEl.innerHTML = "";
		try {
			const res = await fetch(`/api/pokemon/${encodeURIComponent(name)}`);
			if (!res.ok) throw new Error("Not found");
			const data = await res.json();
			renderResult(data);
		} catch (err) {
			showError("Pokémon not found or server error.");
		}
	});
})();
