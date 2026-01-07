def sort(unsorted):
	"""Bidirectional bubble sort that alternates forward and backward passes."""
	n = len(unsorted)
	if n <= 1:
		return unsorted

	a = list(unsorted)
	start = 0
	end = n - 1
	swapped = True

	while swapped:
		swapped = False
		for i in range(start, end):
			if a[i] > a[i + 1]:
				a[i], a[i + 1] = a[i + 1], a[i]
				swapped = True

		if not swapped:
			break

		swapped = False
		end -= 1

		for i in range(end - 1, start - 1, -1):
			if a[i] > a[i + 1]:
				a[i], a[i + 1] = a[i + 1], a[i]
				swapped = True

		start += 1

	return a

timeComplexity = "O(n²)"
spaceComplexity = "O(n)"
variantOf = "bubble"