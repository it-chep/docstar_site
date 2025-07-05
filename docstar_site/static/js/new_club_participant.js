let isLoading = false;


function disableTextSelection(targets){
    targets.forEach(target => {
        target.addEventListener('mousedown', (e) => {
            e.preventDefault()
        })
    })
}


function initTagsInput(options) {
    const container = document.getElementById(options.containerId);
    const tagsList = container.querySelector(`.${options.tagsListClass}`);
    const input = container.querySelector(`.${options.inputClass}`);
    const dropdown = container.querySelector(`.${options.dropdownClass}`);

    if (!container || !tagsList || !input || !dropdown) {
        console.error(`Не найден обязательный элемент для ${options.containerId}`);
        return;
    }

    let allItems = [];
    const selectedItems = [];

    function loadItems() {
        $.ajax({
            url: options.apiUrl,
            type: "GET",
            success: function(response) {
                allItems = response.cities || response.specialities || [];
            },
            error: function(xhr, status, error) {
                console.error('Ошибка загрузки данных:', error);
                allItems = [];
            }
        });
    }

    function updatePlaceholder() {
        input.placeholder = selectedItems.length > 0 ? '' : options.placeholder;
    }

       function addItem(item) {
        if (selectedItems.some(i => options.getItemId(i) === options.getItemId(item))) return;

        selectedItems.push(item);
        renderTag(item);
        updatePlaceholder();
    }

    function renderTag(item) {
        const tagEl = document.createElement('div');
        tagEl.className = 'tag-item';
        tagEl.setAttribute(`data-${options.dataAttrName}`, options.getItemId(item));
        tagEl.innerHTML = `
            ${options.getItemName(item)}
            <span class="tag-remove">×</span>
        `;

        tagEl.addEventListener('click', function(e) {
            if (e.target.classList.contains('tag-remove')) {
                e.stopPropagation();
                removeItem(item);
            }
        });

        tagsList.insertBefore(tagEl, input);
    }

    function removeItem(item) {
        selectedItems.splice(selectedItems.findIndex(
            i => options.getItemId(i) === options.getItemId(item)
        ), 1);

        const tagEl = tagsList.querySelector(
            `.tag-item[data-${options.dataAttrName}="${options.getItemId(item)}"]`
        );
        if (tagEl) tagEl.remove();

        input.focus();
        updatePlaceholder();
    }

    input.addEventListener('keydown', function(e) {
        if (e.key === 'Backspace' && this.value === '' && selectedItems.length > 0) {
            removeItem(selectedItems[selectedItems.length - 1]);
            e.preventDefault();
        }
    });

    function showAutocomplete(items) {
        dropdown.innerHTML = '';
        if (items.length === 0) {
            dropdown.style.display = 'none';
            return;
        }

        items.forEach(item => {
            const div = document.createElement('div');
            div.className = 'autocomplete-item';
            div.textContent = options.getItemName(item);
            div.dataset[options.dataAttrName] = options.getItemId(item);

            div.addEventListener('click', () => {
                addItem(item);
                input.value = '';
                dropdown.style.display = 'none';
                input.focus();
            });

            dropdown.appendChild(div);
        });

        dropdown.style.display = 'block';
    }

    input.addEventListener('input', function() {
        const searchText = this.value.toLowerCase();
        if (!searchText) {
            dropdown.style.display = 'none';
            return;
        }

        const filtered = allItems.filter(item =>
            options.getItemName(item).toLowerCase().includes(searchText) &&
            !selectedItems.some(i => options.getItemId(i) === options.getItemId(item))
        );

        showAutocomplete(filtered);
    });

    document.addEventListener('click', (e) => {
        if (!container.contains(e.target)) {
            dropdown.style.display = 'none';
        }
    });

    loadItems();
    updatePlaceholder();
}

function getSpecialties(){
    let specialties = []
    $('.tags-list.specialties-list [data-specialtyid]').each(function () {
        specialties.push($(this).data('specialtyid'))
    })
    return specialties.join(',')
}

function getCities(){
    let cities = []
    $('.tags-list.cities-list [data-cityid]').each(function () {
        cities.push($(this).data('cityid'))
    })
    return cities.join(',')
}


function initCities() {
    initTagsInput({
        containerId: 'additional_cities',
        apiUrl: '/api/v1/cities_list/',
        inputClass: 'city-input',
        dropdownClass: 'city-dropdown',
        tagsListClass: 'cities-list',
        placeholder: 'Введите название города...',
        getItemName: city => city.city_name,
        getItemId: city => city.city_id,
        dataAttrName: 'cityId'
    });
}
function initSpecialities() {
    initTagsInput({
        containerId: 'additional_specialties',
        apiUrl: '/api/v1/specialities_list/',
        inputClass: 'specialty-input',
        dropdownClass: 'specialty-dropdown',
        tagsListClass: 'specialties-list',
        placeholder: 'Введите название специальности...',
        getItemName: specialty => specialty.speciality_name,  // с бека слово с i
        getItemId: specialty => specialty.speciality_id, // с бека слово с i
        dataAttrName: 'specialtyId'
    });
}

$(document).ready(function () {

    initCities()
    initSpecialities()
    disableTextSelection([document.querySelector('.checkbox-text')])

    $(".submit-button-container").on("click", function () {
        if(isLoading){
            return
        }
        isLoading = true;
        let formData = $("#create-doctor-form").serialize();
        formData += '&additional_cities=' + getCities()
        formData += '&additional_specialties=' + getSpecialties()

        $.ajax({
            url: "/api/v1/create_new_doctor/",
            type: "POST",
            data: formData,
            success: function (response) {
                isLoading = false;
                window.location.href = response.redirect_url;
            },
            error: function (response, status, error) {
                isLoading = false;
                const errors = response.responseJSON.errors;
                if (errors) {
                    displayErrors(errors);
                    $('html, body').animate({scrollTop: 0}, 'slow');
                }
                const Alert = response.responseJSON.alert
                if (Alert) {
                    console.log(Alert);
                }

            },
        });
    });

    initSelect2Fields();
});

function displayErrors(errors) {
    $(".error-message").remove();
    $(".input-wrapper.error").removeClass('error');
    for (const [field, messages] of Object.entries(errors)) {
        const errorMessage = messages.join(", ");
        const inputElement = $(`[name=${field}]`);
        const inputWrapper = inputElement.closest('.input-wrapper')
        inputWrapper.addClass('error')
        if (inputElement.length) {
            inputWrapper.after(`<div class="error-message">${errorMessage}</div>`);
        }
    }
}

function initSelect2Fields() {
    $('[name=city]').select2({
        width: '100%',
        theme: 'dark',
        language: 'ru',
        placeholder: 'Нажмите чтобы открыть поиск города',
        ajax: {
            url: '/api/v1/select2/cities/',
            dataType: 'json',
            delay: 250,
            data: function (params) {
                return {
                    q: params.term || '',
                };
            },
            processResults: function (data) {
                return {
                    results: data.results.map(function (city) {
                        return {
                            id: city.id,
                            text: city.name
                        };
                    })
                };
            },
            cache: true
        },
        minimumInputLength: 1,
    });

    $('[name=speciallity]').select2({
        width: '100%',
        theme: 'dark',
        language: 'ru',
        placeholder: 'Нажмите чтобы открыть поиск специальности',
        ajax: {
            url: '/api/v1/select2/specialities/',
            dataType: 'json',
            delay: 250,
            data: function (params) {
                return {
                    q: params.term || '',
                };
            },
            processResults: function (data) {
                return {
                    results: data.results.map(function (speciality) {
                        return {
                            id: speciality.id,
                            text: speciality.name
                        };
                    })
                };
            },
            cache: true
        },
        minimumInputLength: 1,
    });
    $(document).on('select2:open', function (e) {
        $('.select2-search__field').attr('placeholder', 'Введите текст для поиска...');
        setTimeout(() => {
            const searchField = document.querySelector('.select2-search__field');
            if (searchField) {
                searchField.focus();
            }
        }, 0);
    });
}

function initDatePickerField() {
    $('.datepicker').datepicker({
        format: 'dd.mm.yyyy', // Формат даты
        autoclose: true,      // Закрывать календарь после выбора
        todayHighlight: true, // Подсветка текущей даты
        language: 'ru',       // Локализация на русский
        endDate: '0d'         // Запрет выбора будущих дат
    });
}




document.addEventListener('DOMContentLoaded', function() {
  const container = document.querySelector('.tags-input-container');
  const tagsList = document.querySelector('.tags-list');
  const input = document.querySelector('.tags-input');
  const dropdown = document.querySelector('.autocomplete-dropdown');

  if (!container || !tagsList || !input || !dropdown) {
    console.error('Required elements not found');
    return;
  }

  const allOptions = ['JavaScript', 'TTTTTT', 'SSSSSSSSSS', 'BBBBBBBBBBB', 'Python', 'Java', 'C#', 'PHP', 'Ruby', 'Go', 'GGGGGGG', 'HHHHHHHHHH'];
  const selectedTags = [];

  function showAutocomplete(items) {
    dropdown.innerHTML = '';

    if (items.length === 0) {
      dropdown.style.display = 'none';
      return;
    }

    items.forEach(item => {
      const div = document.createElement('div');
      div.className = 'autocomplete-item';
      div.textContent = item;

      div.addEventListener('click', () => {
        addTag(item);
        input.value = '';
        dropdown.style.display = 'none';
        input.focus();
      });

      dropdown.appendChild(div);
    });

    dropdown.style.display = 'block';
  }


  function updatePlaceholder() {
    if (selectedTags.length > 0) {
      input.placeholder = '';
    } else {
      input.placeholder = 'Поиск...';
    }
  }

  function addTag(tag) {
    if (selectedTags.includes(tag)) return;

    selectedTags.push(tag);

    const tagEl = document.createElement('div');
    tagEl.className = 'tag-item';
    tagEl.innerHTML = `
      ${tag}
      <span class="tag-remove" data-tag="${tag}">×</span>
    `;

    tagEl.addEventListener('click', function(e) {
      if (e.target.classList.contains('tag-remove')) {
        removeTag(e.target.dataset.tag);
      }
    });

    tagsList.insertBefore(tagEl, input);
     updatePlaceholder(); // Обновляем placeholder после добавления
  }

  function removeTag(tag) {
    const index = selectedTags.indexOf(tag);
    if (index !== -1) {
      selectedTags.splice(index, 1);
      const tagEl = tagsList.querySelector(`.tag-item [data-tag="${tag}"]`)?.parentNode;
      if (tagEl) {
        tagEl.remove();
      }
    }
    input.focus();
     updatePlaceholder(); // Обновляем placeholder после удаления
  }

  input.addEventListener('input', function() {
      if (this.value === '' && selectedTags.length === 0) {
      this.placeholder = 'Поиск...';
      }

    const searchText = this.value.toLowerCase();

    if (!searchText) {
      dropdown.style.display = 'none';
      return;
    }

    const filtered = allOptions.filter(option =>
      option.toLowerCase().includes(searchText) &&
      !selectedTags.includes(option)
    );

    showAutocomplete(filtered);
  });

  input.addEventListener('keydown', (e) => {
    if (e.key === 'Backspace' && !input.value && selectedTags.length > 0) {
      removeTag(selectedTags[selectedTags.length - 1]);
    }
    if (e.key === 'Escape') {
      dropdown.style.display = 'none';
    }
  });

  document.addEventListener('click', (e) => {
    if (!container.contains(e.target)) {
      dropdown.style.display = 'none';
    }
  });
});